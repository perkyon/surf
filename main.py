import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN
from commands import register_handlers_common
from schedules import start_scheduled_tasks

# Настройка уровня логирования INFO
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

async def send_welcome_message(message: types.Message):
    # Добавьте логирование в функции send_welcome_message
    logging.info("Обрабатывается команда /start")
    welcome_message = "Приветственное сообщение"
    await message.reply(welcome_message)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    # Регистрация обработчиков команд
    register_handlers_common(dp)

    # Запуск запланированных задач с передачей chat_id
    chat_id = '-1001960802362' 
    await start_scheduled_tasks(bot, chat_id)
    
    # Запуск long polling
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
