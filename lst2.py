import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = ""

# Создание экземпляров Bot, Dispatcher и MemoryStorage
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояние для добавления элемента в список
add_state = dp.current_state()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот для создания списка покупок. Напиши /add, чтобы добавить элемент в список.")

# Обработчик команды /add
@dp.message_handler(commands=['add'])
async def add_item(message: types.Message):
    await message.reply("Введите элемент для добавления в список покупок:")
    await add_state.set()  # Установка состояния для добавления элемента

# Обработчик нового элемента списка
@dp.message_handler(state=add_state)
async def handle_new_item(message: types.Message):
    new_item = message.text
    # Добавление элемента в список покупок
    # (здесь можно добавить код для сохранения элемента, например, в базе данных)
    await message.reply(f"Элемент '{new_item}' успешно добавлен в список покупок.")
    await add_state.reset()  # Сброс состояния

# Запуск бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())