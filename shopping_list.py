import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

# импорт клавиатуры
from keyboard import item_kb, cart_kb, new_cart_bt, connect_cart_bt, add_item_bt, remove_item_bt, show_item_bt

TOKEN = "6160888297:AAH5KdnfEt0aPINbu8KwzwaQKhqJB3qjoAI"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

shopping_carts: list[list] = list() # список со списками покупок разных пользователей
user_mapping: dict[int, int] = dict() # словарь id-пользователей(ключ) - id-корзины(значение)

# Обработчик команды /start
@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await message.reply("Привет! Я бот для создания списка покупок.\n"
                        "Ты можешь создать новую корзину или присоединиться к уже существующей.",
                        reply_markup=cart_kb)
    
@dp.message_handler(Text(equals=new_cart_bt.text), state="*")
@dp.message_handler(commands=['new'], state="*")
async def new(message: types.Message, state: FSMContext):
    cart_id = len(shopping_carts)
    cart = list()
    shopping_carts.append(cart)
    user_mapping[message.from_id] = cart_id
    await message.reply(f"Вот id твоей корзины: {user_mapping[message.from_id]}."
                        " Запомни его и никому не говори!!"
                        " Если ты захочешь присоеденить свою семью, им понадобиться твой id.",
                        reply_markup=item_kb)

# Обработчик команды /connect
@dp.message_handler(Text(equals=connect_cart_bt.text), state="*")
@dp.message_handler(commands=['connect'], state="*")
async def connect(message: types.Message, state: FSMContext):
    await state.set_state("wait_cart_id")
    await message.reply("Введите id корзины:")

@dp.message_handler(state="wait_cart_id")
async def enter_cart_id(message: types.Message, state: FSMContext):
    cart_id = int(message.text)
    if cart_id >= len(shopping_carts) or cart_id < 0:
        await message.reply("Ой-ой (⌣̀_⌣́), такой корзины не сущестует...")
    else:
        user_mapping[message.from_id] = cart_id
        await message.reply("Поздравляю, вы законектились с корзиной! \(★ω★)/", reply_markup=item_kb)
    
    await state.reset_state()

# Обработчик команды /add
@dp.message_handler(Text(equals=add_item_bt.text), state="*")
@dp.message_handler(commands=['add'], state="*")
async def add_item(message: types.Message, state: FSMContext):
    await message.reply("Введите элемент для добавления в список покупок:")
    await state.set_state("wait_item_to_add")

# Обработчик команды /remove
@dp.message_handler(Text(equals = remove_item_bt.text), state="*")
@dp.message_handler(commands=['remove'], state = "*")
async def remove_item(message: types.Message, state: FSMContext):
    cart_id = user_mapping[message.from_id]
    cart = shopping_carts[cart_id]
    if not cart:
        await message.reply("Список покупок ещё пуст((")
    else:
        await message.reply("Введите элемент для удаления:")
        await state.set_state("wait_item_to_remove")

# Обработчик нового элемента списка
@dp.message_handler(state="wait_item_to_add")  
async def handle_new_item(message: types.Message, state: FSMContext):
    new_item = message.text
    cart_id = user_mapping[message.from_id]
    cart = shopping_carts[cart_id]
    cart.append(new_item)
    await message.reply(f"Элемент '{new_item}' добавлен в список покупок!")
    await state.reset_state(with_data=False)

#  Обработчик удаления элемента списка
@dp.message_handler(state="wait_item_to_remove")  
async def handle_remove_item(message: types.Message, state: FSMContext):
    item_to_remove = message.text
    cart_id = user_mapping[message.from_id]
    cart = shopping_carts[cart_id]
    if item_to_remove in cart:
        cart.remove(item_to_remove)
        await message.reply(f"Элемент '{item_to_remove}' удален из списка покупок.")
    else:
        await message.reply("Такого элемента нет в списке покупок.")
    await state.reset_state(with_data=False)


# Обработчик команды /list
@dp.message_handler(Text(equals = show_item_bt.text), state="*")
@dp.message_handler(commands=['list'], state="*")
async def show_list(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cart_id = user_mapping[message.from_id]
    cart = shopping_carts[cart_id]

# проверка пустоты списка
    if not cart:
        await message.reply("Список покупок ещё пуст. [± _ ±]")
    else:
        list_text = "\n".join(cart)
        await message.reply(f"Вот список покупок <3:\n{list_text}")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)