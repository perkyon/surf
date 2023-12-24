import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from work_schedule import is_working_hour, cleanliness_check_intervals
from plants import spray_schedule
from tasks import weekly_tasks

async def send_watering_reminder(bot: Bot, chat_id: str):
    now = datetime.now()
    for plant, info in spray_schedule.items():
        last_watered = now - timedelta(days=info["interval"])
        if last_watered.weekday() == now.weekday():
            await bot.send_message(chat_id, info["message"])

async def send_daily_task_notification(bot: Bot, chat_id: str):
    now = datetime.now()
    current_day = now.strftime("%A").lower()
    tasks_for_today = weekly_tasks.get(current_day, [])
    if tasks_for_today:
        message = f"Сегодня {current_day}, задачи:\n" + "\n".join(f"• {task}" for task in tasks_for_today)
        await bot.send_message(chat_id, message)

async def send_report_reminder(bot: Bot, chat_id: str):
    now = datetime.now()
    if now.weekday() >= 5:  # Выходные
        if (now.hour == 16 and now.minute >= 30) or now.hour == 23:
            await bot.send_message(chat_id, "Пора написать отчет о выполнении задач на сегодня!")
    else:  # Будни
        if (now.hour == 15 and now.minute >= 30) or now.hour == 23:
            await bot.send_message(chat_id, "Пора написать отчет о выполнении задач на сегодня!")

async def scheduled_task_notifications(bot: Bot, chat_id: str):
    while True:
        if is_working_hour():
            now = datetime.now()
            current_day = now.strftime("%A").lower()
            if now.weekday() >= 5:  # Выходные
                if now.hour == 9 or (now.hour == 16 and now.minute >= 30) or now.hour == 23:
                    await send_daily_task_notification(bot, chat_id)
            else:  # Будни
                if now.hour == 7 or (now.hour == 15 and now.minute >= 30) or now.hour == 23:
                    await send_daily_task_notification(bot, chat_id)
        await asyncio.sleep(3600)  # Пауза в 1 час

import work_schedule

async def scheduled_cleanliness_reminders(bot: Bot, chat_id: str):
    while True:
        now = datetime.now()
        current_time = (now.hour, now.minute)
        if now.weekday() >= 5:  # Выходные
            if current_time in work_schedule.cleanliness_check_intervals["weekend"]:
                await bot.send_message(chat_id, 'Нужно проверить чистоту кофейни')
        else:  # Будние дни
            if current_time in work_schedule.cleanliness_check_intervals["weekday"]:
                await bot.send_message(chat_id, 'Нужно проверить чистоту кофейни')
        await asyncio.sleep(60)  # Пауза в 1 минуту

async def scheduled_report_reminders(bot: Bot, chat_id: str):
    while True:
        if is_working_hour():
            await send_report_reminder(bot, chat_id)
        await asyncio.sleep(1800)  # Пауза в 30 минут


def start_scheduled_tasks(loop: asyncio.AbstractEventLoop, bot: Bot):
    chat_id = '-1001960802362'
    loop.create_task(scheduled_task_notifications(bot, chat_id))
    loop.create_task(scheduled_cleanliness_reminders(bot, chat_id))
    loop.create_task(scheduled_report_reminders(bot, chat_id))