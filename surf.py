import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import locale
from datetime import datetime, timedelta

# Устанавливаем русскую локаль для получения дня недели на русском языке
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

# Вставьте свой токен Telegram-бота здесь
BOT_TOKEN = '6746134454:AAHvuB_hSpTWLJ1j1CET678aQhsrCWrRHAI'

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Список задач на неделю
tasks = {
    "Понедельник": ["Чистка гриндера", "Чистка гейзеров"],
    "Вторник": ["Протереть лайт боксы и вывески", "Вымести листья и мусор под трибуны", "Натереть зеркала"],
    "Среда": ["Чистка гриля и микроволновки", "Заточка ножей", "Протереть пыль (картины, батареи, полки)"],
    "Четверг": ["Уборка на складе", "Чистка гриндера", "Зона витрины (убрать все подносы и замыть, натереть витрину внутри)"],
    "Пятница": ["Протереть лайт боксы, гирлянду и вывеску", "Зона шкафов на баре (протереть полки, расставить продукцию, пополнить необходимое)"],
    "Суббота": ["Чистка термопода кафизой", "Чистка блендера кафизой", "Протереть шкафы сверху"],
    "Воскресенье": ["Почистить большой пылесос", "Протереть пыль (картины, батареи, полки)", "Протереть и помыть низ бара"]
}

spray_schedule = {
    "Юкка": {"interval": 2, "message": "Опрыскать Юкку"},
    "Драцена": {"interval": 2, "message": "Проверить Драцену (Саня и Мия) и опрыскать по необходимости"},
    "Цикас": {"interval": 2, "message": "Открыть и проветрить укрытую пальму (Цикас) на улице"}
}

def is_weekend():
    return datetime.now().weekday() >= 5  # Суббота и Воскресенье

def is_working_hour():
    now = datetime.now()
    hour = now.hour
    if is_weekend():
        return 9 <= hour < 23
    else:
        return 7 <= hour < 23

# Функция для отправки напоминаний о поливе
async def send_watering_reminder(chat_id):
    now = datetime.now()
    for plant, info in spray_schedule.items():
        last_watered = now - timedelta(days=info["interval"])
        if last_watered.weekday() == now.weekday():
            message = info["message"]
            await bot.send_message(chat_id, message)

# Функция для отправки уведомления
async def send_daily_task_notification(chat_id):
    now = datetime.now()
    current_day = now.strftime("%A").capitalize()
    tasks_for_today = tasks.get(current_day, [])
    if tasks_for_today:
        message = f"Сегодня ({current_day}) задачи:\n"
        for task in tasks_for_today:
            message += f"• {task}\n"
        await bot.send_message(chat_id, message)

async def scheduled_task_notifications(chat_id):
    while True:
        now = datetime.now()
        if is_weekend():
            if (now.hour == 10 and now.minute == 0) or (now.hour == 18 and now.minute == 0):
                await send_daily_task_notification(chat_id)
        else:
            if (now.hour == 8 and now.minute == 0) or (now.hour == 17 and now.minute == 0):
                await send_daily_task_notification(chat_id)
        await asyncio.sleep(60)

async def scheduled_cleanliness_reminders(chat_id):
    while True:
        if is_working_hour():
            await bot.send_message(chat_id, 'Нужно проверить чистоту кофейни')
            await asyncio.sleep(7200)  # Пауза в 2 часа
        else:
            await asyncio.sleep(60)  # Пауза в минуту вне рабочего времени

async def send_report_reminder(chat_id):
    now = datetime.now()
    if is_weekend():
        if (now.hour == 16 and now.minute == 0) or (now.hour == 23 and now.minute == 0):
            await bot.send_message(chat_id, "Пора написать отчет о выполнении задач на сегодня!")
    else:
        if (now.hour == 15 and now.minute == 30) or (now.hour == 23 and now.minute == 0):
            await bot.send_message(chat_id, "Пора написать отчет о выполнении задач на сегодня!")

async def scheduled_report_reminders(chat_id):
    while True:
        await send_report_reminder(chat_id)
        await asyncio.sleep(60)

# Обработчик команды /id
@dp.message_handler(commands=['id'])
async def send_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"ID этого чата: {chat_id}")

if __name__ == '__main__':
    chat_id = '-1001960802362'
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_task_notifications(chat_id))
    loop.create_task(scheduled_cleanliness_reminders(chat_id))
    loop.create_task(scheduled_report_reminders(chat_id))
    executor.start_polling(dp, skip_updates=True)