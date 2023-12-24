# Файл который мы должны запускать
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
from config import BOT_TOKEN
import commands
import schedules

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

commands.register_handlers_common(dp)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    schedules.start_scheduled_tasks(loop, bot)
    executor.start_polling(dp, skip_updates=True)
