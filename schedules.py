import asyncio
from aiogram import Bot
from datetime import datetime
from data import spray_schedule, weekly_tasks, report_reminder_times, cleanliness_check_intervals, daily_task_times
from utils import (should_send_watering_reminder, should_send_daily_task_notification,
                   should_send_report_reminder, should_send_cleanliness_reminder, send_message)
import logging  # Добавьте импорт модуля logging

# Настройка уровня логирования
logging.basicConfig(level=logging.INFO)

async def start_scheduled_tasks(bot: Bot, chat_id: str):
    logging.info("Запуск запланированных задач")
    while True:
        now = datetime.now()

        # Напоминание о поливе
        tasks = should_send_watering_reminder(now, spray_schedule)
        for task in tasks:
            await send_message(bot, chat_id, task["message"])
            task["last_watered"] = now  # Обновляем время последнего полива
        
        # Отправка ежедневных задач
        task_message = should_send_daily_task_notification(now, weekly_tasks)
        if task_message:
            await send_message(bot, chat_id, task_message)

        # Напоминание об отчетах
        if should_send_report_reminder(now, report_reminder_times):
            await send_message(bot, chat_id, "Пора написать отчет о выполнении задач на сегодня!")

        # Напоминание о проверке чистоты
        if should_send_cleanliness_reminder(now, cleanliness_check_intervals):
            await send_message(bot, chat_id, "Нужно проверить чистоту кофейни")

        await asyncio.sleep(60)  # Пауза в 60 секунд между проверками
