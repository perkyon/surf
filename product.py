from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Определение состояний для формы добавления продукта
class ProductForm(StatesGroup):
    name = State()  # Название продукта
    expiration_date = State()  # Срок годности

# Команда для начала диалога добавления продукта
async def cmd_add_product(message: types.Message):
    await ProductForm.name.set()
    await message.answer("Введите название продукта:")

# Обработчик для названия продукта
async def process_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await ProductForm.next()
    await message.answer("Введите дату истечения срока годности (дд.мм.гггг):")

# Обработчик для срока годности продукта
async def process_expiration_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['expiration_date'] = message.text
        # Здесь код для сохранения данных в базу данных или другое хранилище
    await state.finish()
    await message.answer(f"Продукт {data['name']} с сроком годности {data['expiration_date']} добавлен.")

# Функция для регистрации обработчиков
def register_handlers_product(dp: Dispatcher):
    dp.register_message_handler(cmd_add_product, commands=['add_product'], state="*")
    dp.register_message_handler(process_product_name, state=ProductForm.name)
    dp.register_message_handler(process_expiration_date, state=ProductForm.expiration_date)
