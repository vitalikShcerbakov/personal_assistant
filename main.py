import logging.config
import sqlite3
import sys

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import openai
from roles import messages
from settings import MY_ID, OPENAI_TOKEN, TELEGRAM_TOKEN, WHITE_USERS

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

telegram_token = TELEGRAM_TOKEN
openai.api_key = OPENAI_TOKEN


# подключение к базе данных
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

# создаем таблицу, если ее нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        chat_id INTEGER,
        message TEXT,
        answer TEXT,
        date TEXT
    )
''')
conn.commit()


bot = Bot(telegram_token)
dp = Dispatcher(bot)


def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Это простой телеграм-бот на Python!')


@dp.message_handler()
async def send(message: types.Message):
    update(messages, "user", message.text)
    if not message.from_user.id in WHITE_USERS:
        logger.critical(f'{message.from_user.full_name} с id {message.from_user.id} зашел к нам в чат) ')
        await bot.send_message(MY_ID, f'{message.from_user.full_name} с id {message.from_user.id} зашел к нам в чат)')
        await bot.send_message(MY_ID, WHITE_USERS)
        # return
    answer = None
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Новая модель с контекстом
            messages=messages,   # База данных на основе словаря
        )
        answer = response['choices'][0]['message']['content']
        await message.answer(answer, parse_mode="markdown")
        messages.append({"role": "assistant", "content": answer})
    except Exception as error:
        await message.answer(
            f'Что то пошло не так, вот ошибка: {error}', parse_mode="markdown"
            )
        logger.critical(
            f'Critical error! А вот и сама ошибка: {error}')
        sys.exit()

    try:
        # Сохранение сообщений в БД
        cursor.execute('''
            INSERT INTO messages (user_id, chat_id, message, answer, date)
            VALUES (?, ?, ?, ?, ?)''', (message.from_user.id, message.chat.id,
                                        message.text,
                                        answer,
                                        message.date))
        conn.commit()
        logger.info('The message was successfully written to the database')
    except Exception as error:
        logger.error(f'error writing to database: {error}')


if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as error:
            logger.critical(f'An error has occurred{error}')
