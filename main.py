# Файл который мы должны запускать
import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, state
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import commands
import schedules

from config import BOT_TOKEN

import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

commands.register_handlers_common(dp)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    schedules.start_scheduled_tasks(loop, bot)
    executor.start_polling(dp, skip_updates=True)
