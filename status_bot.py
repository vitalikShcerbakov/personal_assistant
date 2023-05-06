import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
# Инициализация монитора лог-файлов
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Исправления ИИ
import tracemalloc
tracemalloc.start()

from settings import STATUS_TELEGRAM_TOKEN, MY_ID


TOKEN = STATUS_TELEGRAM_TOKEN  # Замените YOUR_TOKEN_HERE на свой токен бота Telegram
CHAT_ID = MY_ID  # Замените YOUR_CHAT_ID_HERE на свой Chat ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start
    """
    await message.reply("Привет! Я монитор лог-файлов и буду уведомлять вас о любых изменениях.")


async def send_notification(filename: str):
    """
    Функция для отправки уведомления об изменении лог-файла
    """
    message = f"Лог-файл {filename} был изменен!"
    await bot.send_message(chat_id=CHAT_ID, text=message)


class LogFileEventHandler(FileSystemEventHandler):
    async def on_modified(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            # Отправляем уведомление об изменении лог-файла
            await send_notification(event.src_path)


if __name__ == '__main__':
    observer = Observer()
    event_handler = LogFileEventHandler()
    observer.schedule(event_handler, '.', recursive=False)  # Вместо точки можно указать путь к папке с логами
    observer.start()

    # Запускаем бота Telegram
    executor.start_polling(dp, skip_updates=True)