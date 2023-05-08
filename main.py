import logging.config
import sqlite3
import sys

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import psycopg2

import openai
from roles import messages
from settings import MY_ID, OPENAI_TOKEN, TELEGRAM_TOKEN, WHITE_USERS

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

telegram_token = TELEGRAM_TOKEN
openai.api_key = OPENAI_TOKEN


# подключение к базе данных
def database_func(message,answer):
    connection = None
    try:
        # connect to exist database
        connection = psycopg2.connect(
        host="127.0.0.1",
        user="admin",
        database="messages_bot",
        #database="lesson_postgresql",
        password="qwerty",
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            # cursor.execute('SELECT version();') 
            # print(f'Server version: {cursor.fetchone()}')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id serial PRIMARY KEY,
                    user_id INTEGER,
                    nickname VARCHAR(100),
                    chat_id INTEGER,
                    message VARCHAR,
                    answer VARCHAR,
                    date varchar(40)
                )
            ''')
        print('[INFO] table create =)')
        with connection.cursor() as cursor:
            sql_query = """INSERT INTO messages (user_id, nickname, chat_id, message, answer, date)
            VALUES (%s, %s, %s, %s, %s, %s);"""
            data = (message.from_user.id, message.from_user.full_name,
                                        message.chat.id,
                                        message.text,
                                        answer,
                                        message.date)
            cursor.execute(sql_query, data)
        print('[INFO] table value added =)')
             
    except Exception as e:
        print('[INFO] Error vhile working with PostgreSQL', e)
    finally:
        if connection:
            connection.close()
            print('[INFO} PostgreSQL connection closed')




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
        database_func(message, answer)
        #conn.commit()
        logger.info('The message was successfully written to the database')
    except Exception as error:
        logger.error(f'error writing to database: {error}')


if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as error:
            logger.critical(f'An error has occurred{error}')
