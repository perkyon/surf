# Файл который мы должны запускать
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
from config import BOT_TOKEN
import commands
import schedules
import product
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

commands.register_handlers_common(dp)
product.register_handlers_product(dp)  # Регистрация обработчиков из product.py


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    schedules.start_scheduled_tasks(loop, bot)
    executor.start_polling(dp, skip_updates=True)
