from datetime import datetime, timedelta
from aiogram import Bot
import logging

def should_send_watering_reminder(now, spray_schedule):
    reminders = []
    for plant, info in spray_schedule.items():
        if now >= info["last_watered"] + timedelta(days=info["interval"]):
            reminders.append(info)
    return reminders

def should_send_daily_task_notification(now, weekly_tasks):
    current_day = now.strftime("%A").lower()
    tasks_for_today = weekly_tasks.get(current_day, [])
    if tasks_for_today:
        message = f"Сегодня {current_day}, задачи:\n"
        for task in tasks_for_today:
            message += f"- {task['task']}\n"
        return message
    return ""

def should_send_report_reminder(now, report_reminder_times):
    current_time_str = now.strftime("%H:%M")
    current_day_type = "weekend" if now.weekday() >= 5 else "weekday"
    return current_time_str in report_reminder_times[current_day_type]

def should_send_cleanliness_reminder(now, cleanliness_check_intervals):
    current_time = (now.hour, now.minute)
    current_day_type = "weekend" if now.weekday() >= 5 else "weekday"
    for hour, minute in cleanliness_check_intervals[current_day_type]:
        if current_time == (hour, minute):
            return True
    return False

async def send_message(bot: Bot, chat_id: str, message: str):
    logging.info(f"Сообщение успешно отправлено: {message}")
    await bot.send_message(chat_id, message)
