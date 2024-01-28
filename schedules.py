import asyncio
from aiogram import types
from datetime import datetime, timedelta
from aiogram import Bot
from work_schedule import report_reminder_times, cleanliness_check_intervals, daily_task_times
from plants import spray_schedule
from tasks import weekly_tasks
from work_schedule import is_working_hour
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import dp


# Функция для отправки напоминаний о поливе
async def send_watering_reminder(bot: Bot, chat_id: str):
    now = datetime.now()
    for plant, info in spray_schedule.items():
        # Проверяем, пришло ли время для полива
        if now >= info["last_watered"] + timedelta(days=info["interval"]):
            await bot.send_message(chat_id, info["message"])
            # Обновляем время последнего полива
            info["last_watered"] = now

# Функция для отправки ежедневных задач
async def send_daily_task_notification(bot: Bot, chat_id: str):
    now = datetime.now()
    current_day = now.strftime("%A").lower()
    tasks_for_today = weekly_tasks.get(current_day, [])
    if tasks_for_today:
        message = f"Сегодня {current_day}, задачи:\n" + "\n".join(f"• {task}" for task in tasks_for_today)
        await bot.send_message(chat_id, message)

# Функция для отправки напоминаний об отчетах
async def send_report_reminder(bot: Bot, chat_id: str):
    message = "Пора написать отчет о выполнении задач на сегодня!"
    await bot.send_message(chat_id, message)

# Функция для отправки напоминаний о проверке чистоты
async def scheduled_cleanliness_reminders(bot: Bot, chat_id: str):
    message = "Нужно проверить чистоту кофейни"
    await bot.send_message(chat_id, message)

# Функции проверки времени для отправки напоминаний
def should_send_watering_reminder(now: datetime) -> bool:
    # Задаем время напоминания
    scheduled_time = now.replace(hour=18, minute=0, second=0, microsecond=0)
    # Проверяем, что текущее время соответствует времени запланированного напоминания
    return now >= scheduled_time and now < scheduled_time + timedelta(minutes=1)

def should_send_daily_task_notification(now: datetime) -> bool:
    current_time_str = now.strftime("%H:%M")
    current_day_type = "weekend" if now.weekday() >= 5 else "weekday"
    return current_time_str in daily_task_times[current_day_type]

def should_send_report_reminder(now: datetime) -> bool:
    current_time_str = now.strftime("%H:%M")
    current_day_type = "weekend" if now.weekday() >= 5 else "weekday"
    return current_time_str in report_reminder_times[current_day_type]

def should_send_cleanliness_reminder(now: datetime) -> bool:
    current_time = (now.hour, now.minute)
    current_day_type = "weekend" if now.weekday() >= 5 else "weekday"
    return current_time in cleanliness_check_intervals[current_day_type]

# Планировщик для автоматической отправки напоминаний
async def scheduler(bot: Bot, chat_id: str):
    while True:
        now = datetime.now()

        if should_send_watering_reminder(now):
            await send_watering_reminder(bot, chat_id)
        if should_send_daily_task_notification(now):
            await send_daily_task_notification(bot, chat_id)
        if should_send_report_reminder(now):
            await send_report_reminder(bot, chat_id)
        if should_send_cleanliness_reminder(now):
            await scheduled_cleanliness_reminders(bot, chat_id)

        await asyncio.sleep(60)  # Пауза в 1 минуту

def should_send_cleanliness_reminder(now: datetime) -> bool:
    if not is_working_hour():
        return False
    current_time = (now.hour, now.minute)
    current_day_type = "weekend" if now.weekday() >= 5 else "weekday"
    return current_time in cleanliness_check_intervals[current_day_type]

def start_scheduled_tasks(loop: asyncio.AbstractEventLoop, bot: Bot):
    chat_id = '-1001960802362'  # ID чата для отправки напоминаний
    loop.create_task(scheduler(bot, chat_id))

@dp.callback_query_handler(lambda query: query.data.startswith('task_toggle_'))
async def toggle_task_status(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    day = data[2]
    task_text = '_'.join(data[3:])

    # Измените статус задачи (поменяйте True на False и наоборот)
    for task_info in weekly_tasks[day]:
        if task_info["task"] == task_text:
            task_info["completed"] = not task_info.get("completed", False)

    # Обновите сообщение с задачами (повторно отправьте сообщение)
    await weekly_tasks(callback_query.message.chat.id)

    # Ответьте на callback, чтобы убрать индикатор загрузки
    await callback_query.answer()

