import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import locale

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
    "понедельник": ["Чистка гриндера", "Чистка гейзеров", "Замачивание форсунок и их чистка"],
    "вторник": ["Протереть лайт боксы и вывески", "Вымести листья и мусор под трибуны", "Натереть зеркала", "Замачивание форсунок и их чистка"],
    "среда": ["Чистка гриля и микроволновки", "Заточка ножей", "Протереть пыль (картины, батареи, полки)", "Замачивание форсунок и их чистка"],
    "четверг": ["Уборка на складе", "Чистка гриндера", "Зона витрины (убрать все подносы и замыть, натереть витрину внутри)", "Замачивание форсунок и их чистка"],
    "пятница": ["Протереть лайт боксы, гирлянду и вывеску", "Зона шкафов на баре (протереть полки, расставить продукцию, пополнить необходимое)", "Замачивание форсунок и их чистка"],
    "суббота": ["Чистка термопода кафизой", "Чистка блендера кафизой", "Протереть шкафы сверху", "Замачивание форсунок и их чистка"],
    "воскресенье": ["Почистить большой пылесос", "Протереть пыль (картины, батареи, полки)", "Протереть и помыть низ бара", "Замачивание форсунок и их чистка"]
}

# Цветы и опрыскивание 
spray_schedule = {
    "Юкка": {"interval": 2, "message": "Опрыскать Юкку"},
    "Драцена": {"interval": 2, "message": "Проверить Драцену (Саня и Мия) и опрыскать по необходимости"},
    "Цикас": {"interval": 2, "message": "Открыть и проветрить укрытую пальму (Цикас) на улице"}
}

# Вспомогательные функции
def is_weekend():
    return datetime.now().weekday() >= 5  # Суббота и Воскресенье

def is_working_hour():
    now = datetime.now()
    hour = now.hour
    return 9 <= hour < 23 if is_weekend() else 7 <= hour < 23

# Асинхронные функции для отправки напоминаний
async def send_watering_reminder(chat_id):
    now = datetime.now()
    for plant, info in spray_schedule.items():
        last_watered = now - timedelta(days=info["interval"])
        if last_watered.weekday() == now.weekday():
            await bot.send_message(chat_id, info["message"])

async def send_daily_task_notification(chat_id):
    now = datetime.now()
    current_day = now.strftime("%A").lower()
    tasks_for_today = tasks.get(current_day, [])
    if tasks_for_today:
        message = f"Сегодня {current_day}, задачи:\n" + "\n".join(f"• {task}" for task in tasks_for_today)
        await bot.send_message(chat_id, message)

async def scheduled_task_notifications(chat_id):
    while True:
        if is_weekend():
            if datetime.now().hour in [10, 18]:
                await send_daily_task_notification(chat_id)
        else:
            if datetime.now().hour in [8, 17]:
                await send_daily_task_notification(chat_id)
        await asyncio.sleep(3600)  # Пауза в 1 час

async def scheduled_cleanliness_reminders(chat_id):
    while True:
        if is_working_hour():
            await bot.send_message(chat_id, 'Нужно проверить чистоту кофейни')
            await asyncio.sleep(7200)  # Пауза в 2 часа
        else:
            await asyncio.sleep(3600)  # Пауза в 1 час вне рабочего времени

async def send_report_reminder(chat_id):
    now = datetime.now()
    if is_weekend():
        if now.hour in [16, 23]:
            await bot.send_message(chat_id, "Пора написать отчет о выполнении задач на сегодня!")
    else:
        if now.hour in [15, 23] and now.minute >= 30:
            await bot.send_message(chat_id, "Пора написать отчет о выполнении задач на сегодня!")

async def scheduled_report_reminders(chat_id):
    while True:
        await send_report_reminder(chat_id)
        await asyncio.sleep(1800)  # Пауза в 30 минут

async def scheduled_watering_reminders(chat_id):
    while True:
        await send_watering_reminder(chat_id)
        await asyncio.sleep(86400)  # Пауза в 24 часа

# Обработчик команды /id
@dp.message_handler(commands=['id'])
async def send_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"ID этого чата: {chat_id}")

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome_message(message: types.Message):
    welcome_message = (
        "🌊 Привет, друзья-серферы! 🏄‍♂️\n\n"
        "🏄‍♂️ Я ваш новый помощник-бот, здесь, чтобы делать ваше приключение на волнах еще более незабываемым! "
        "Буду рад помогать вам с полезными напоминаниями и заботиться о том, чтобы наш любимый спот оставался чистым и приятным для всех.\n\n"
        "🤖 Хочешь узнать больше о моих функциях? Просто отправь команду /help и я покажу тебе все, что умею!\n\n"
        "🔍 Есть вопросы или нужна помощь? Не стесняйся обращаться к моему создателю @ilyafomintsev - он всегда на связи, чтобы сделать наше общение еще лучше."
    )
    await message.reply(welcome_message)

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help_message(message: types.Message):
    help_message = (
        "👋 Вот что я могу делать:\n\n"
        "1️⃣ Отправлять ежедневные напоминания о задачах на день.\n"
        "2️⃣ Напоминать о необходимости проверки чистоты кофейни каждые два часа.\n"
        "3️⃣ Напоминать о поливе растений по расписанию.\n"
        "4️⃣ Напоминать о написании отчетов о выполненных задачах.\n\n"
        "📅 Я также могу напоминать тебе о задачах в зависимости от дня недели.\n\n"
        "🤖 Нужна помощь или есть предложения? Обращайся к моему создателю @ilyafomintsev"
    )
    await message.reply(help_message)

if __name__ == '__main__':
    chat_id = 'YOUR_CHAT_ID'
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_task_notifications(chat_id))
    loop.create_task(scheduled_cleanliness_reminders(chat_id))
    loop.create_task(scheduled_report_reminders(chat_id))
    loop.create_task(scheduled_watering_reminders(chat_id))
    executor.start_polling(dp, skip_updates=True)
