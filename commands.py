from aiogram import types, Dispatcher

async def send_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"ID этого чата: {chat_id}")

async def send_welcome_message(message: types.Message):
    welcome_message = (
        "🌊 Привет, друзья-серферы! 🏄‍♂️\n\n"
        "🏄‍♂️ Я ваш новый помощник-бот, здесь, чтобы делать ваше приключение на волнах еще более незабываемым! "
        "Буду рад помогать вам с полезными напоминаниями и заботиться о том, чтобы наш любимый спот оставался чистым и приятным для всех.\n\n"
        "🤖 Хочешь узнать больше о моих функциях? Просто отправь команду /help и я покажу тебе все, что умею!\n\n"
        "🔍 Есть вопросы или нужна помощь? Не стесняйся обращаться к моему создателю @ilyafomintsev - он всегда на связи, чтобы сделать наше общение еще лучше."
    )
    await message.reply(welcome_message)

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



def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(send_chat_id, commands=['id'])
    dp.register_message_handler(send_welcome_message, commands=['start'])
    dp.register_message_handler(send_help_message, commands=['help'])
