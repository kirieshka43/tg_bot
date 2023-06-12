"""
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
# Замените "YOUR_BOT_TOKEN" на токен вашего бота
TOKEN = ""

# Создание экземпляров Bot и Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Словарь для хранения списка покупок
shopping_list = []

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот для создания списка покупок. Напиши /add, чтобы добавить элемент в список.")

# Обработчик команды /add
@dp.message_handler(commands=['add'])
async def add_item(message: types.Message):
    await message.reply("Введите элемент для добавления в список покупок:")
    dp.register_message_handler(handle_new_item, state="*")  # Регистрация обработчика для следующего сообщения

# Обработчик нового элемента списка
async def handle_new_item(message: types.Message):
    new_item = message.text
    shopping_list.append(new_item)

    await message.reply(f"Элемент '{new_item}' успешно добавлен в список покупок.")


@dp.message_handler(commands=['delete'])
async def delete_item(message: types.Message, state: FSMContext):
    await message.reply("Введите элемент для удаления из списка покупок:")
    old_item = message.text
    shopping_list.remove(old_item)
    await state.set_state("enter_to_delete")


@dp.message_handler(state="enter_to_delete")
async def handle_old_item(message: types.Message):
    old_item = message.text
    shopping_list.remove(old_item)
    await message.reply(f"Элемент '{old_item}' успешно удалён из списка покупок.")
    await state.set_state("be nice")

@dp.message_handler(state="be nice")
async def handle_old_item(message: types.Message):
    await message.reply("You are veeeeery cute!")

# Обработчик команды /list
@dp.message_handler(commands=['list'])
async def show_list(message: types.Message):
    if not shopping_list:
        await message.reply("Список покупок пуст.")
    else:
        list_text = "\n".join(shopping_list)
        await message.reply(f"Список покупок:\n{list_text}")    

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling())
    """
import asyncio
from aiogram import Bot, Dispatcher, types

# Замените "YOUR_BOT_TOKEN" на токен вашего бота
TOKEN = "6160888297:AAH5KdnfEt0aPINbu8KwzwaQKhqJB3qjoAI"

# Создание экземпляров Bot и Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Словарь для хранения списка покупок
shopping_list = []

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот для создания списка покупок. Напиши /add, чтобы добавить элемент в список.")

# Обработчик команды /add
@dp.message_handler(commands=['add'])
async def add_item(message: types.Message):
    await message.reply("Введите элемент для добавления в список покупок:")
    dp.register_message_handler(handle_new_item, state="*")  # Регистрация обработчика для следующего сообщения

# Обработчик нового элемента списка
async def handle_new_item(message: types.Message):
    new_item = message.text
    shopping_list.append(new_item)

    await message.reply(f"Элемент '{new_item}' успешно добавлен в список покупок.")

# Обработчик команды /remove
@dp.message_handler(commands=['remove'])
async def remove_item(message: types.Message):
    if not shopping_list:
        await message.reply("Список покупок пуст.")
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        buttons = [types.KeyboardButton(item) for item in shopping_list]
        keyboard.add(*buttons)

        await message.reply("Выберите элемент для удаления:", reply_markup=keyboard)
        dp.register_message_handler(handle_remove_item, state="*")  # Регистрация обработчика для следующего сообщения

# Обработчик удаления элемента списка
async def handle_remove_item(message: types.Message):
    item_to_remove = message.text

    if item_to_remove in shopping_list:
        shopping_list.remove(item_to_remove)
        await message.reply(f"Элемент '{item_to_remove}' успешно удален из списка покупок.")
    else:
        await message.reply("Выбранный элемент не найден в списке покупок.")

# Запуск бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())