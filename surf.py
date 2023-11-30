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

async def scheduled_watering_notifications(chat_id):
    while True:
        now = datetime.now()
        if 7 <= now.hour < 23:
            await send_watering_reminder(chat_id)
        # Пауза в 1 час (3600 секунд)
        await asyncio.sleep(3600)


# Функция для отправки уведомления о необходимости написать отчет
async def send_report_reminder(chat_id):
    await bot.send_message(chat_id, "Пора написать отчет о выполнении задач на сегодня!")

# Напоминалка каждые 45 минут
async def send_cleanliness_reminder(chat_id):
    while True:
        now = datetime.now()
        if 7 <= now.hour < 23:
            await bot.send_message(chat_id, 'Нужно проверить чистоту кофейни')
        # Пауза в 45 минут (2700 секунд)
        await asyncio.sleep(2700)

# Определяем задачи по расписанию
async def scheduled_task_notifications(chat_id):
    while True:
        now = datetime.now()
        if now.hour == 8 and now.minute == 0:
            await send_daily_task_notification(chat_id)
        elif now.hour == 15 and now.minute == 0:
            await send_report_reminder(chat_id)
        await asyncio.sleep(60)

# Напоминание о поливе
async def scheduled_plant_care_notifications(chat_id):
    while True:
        now = datetime.now()
        if now.hour == 9 and now.minute == 0:  # Например, уведомления о поливе в 9 утра
            await send_watering_reminder(chat_id)
        await asyncio.sleep(60)

if __name__ == '__main__':
    chat_id = '-1001960802362'
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_task_notifications(chat_id))
    loop.create_task(send_cleanliness_reminder(chat_id))
    loop.create_task(scheduled_plant_care_notifications(chat_id))
    loop.create_task(scheduled_watering_notifications(chat_id))  # Добавляем новую задачу
    executor.start_polling(dp, skip_updates=True)

