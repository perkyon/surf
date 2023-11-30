@dp.message_handler()
async def echo_message(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"Your Chat ID is: {chat_id}")