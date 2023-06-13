import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = ""

# Создание экземпляров Bot и Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот 'Выращивание ёлочки'. Напиши мне /tree, чтобы увидеть анимированную ёлочку!")

# Обработчик команды /tree
@dp.message_handler(commands=['tree'])
async def tree(message: types.Message):
    tree_frames = [
        "        🌲\n",
        "      🌲🌲🌲\n",
        "    🌲🌲🌲🌲🌲\n",
        "  🌲🌲🌲🌲🌲🌲🌲\n",
        "🌲🌲🌲🌲🌲🌲🌲🌲🌲\n",
        "        🎄\n",
    ]

    for frame in tree_frames:
        await message.reply(frame, parse_mode="HTML")
        await asyncio.sleep(1)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling())