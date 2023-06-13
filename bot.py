import random
from env import TOKEN

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import logging
logging.basicConfig(level=logging.INFO)


TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

connected_users = []


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    
    connected_users.append(message.from_user.id)
    await message.answer("Hi!\nPlease, say your name")
    await state.set_state("q1")


@dp.message_handler(state = "q1")
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name" : name})
    await state.set_state("q2")
    await message.answer("Say your age")
    
@dp.message_handler(state = "q2")
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if age.isdigit():
        await state.update_data({"age" : int(age)})
        if int(age) < 18:
            await message.answer("I wont work with u!")
        else:
            await state.set_state("ready")
            await message.answer("If u are ready to start search send 'yes'!")

    else:
        data = await state.get_data()
        await message.answer(f"This is not a number, try another time, {data['name']}")



@dp.message_handler(state = "ready")
async def ready(message: types.Message, state: FSMContext):
    ans = message.text
    await state.update_data({"ans" : ans})
    if ans == 'yes' or ans == 'YES' or ans == 'Yes':
        await state.set_state("waiting")
        await message.answer("To search, send '/find'")
    else:
        await message.answer("Bye, bitch")


@dp.message_handler(commands=['find'], state = "waiting")
async def ready(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    targets = set(connected_users) - {user_id, }
    if targets:
        target = random.choice(list(targets))
        target_state: FSMContext = dp.current_state(chat=target, user=target)
        await message.answer(f"Вы связаны с {target_state.user}")
        await bot.send_message(target, f"Вы связаны с {user_id}")
        await state.set_state("connected")
        await target_state.set_state("connected")
        await state.update_data({"buddy": target})
        await target_state.update_data({"buddy": user_id})
        await connected_users.remove(target)
        await connected_users.remove(user_id)
    else:
        await message.answer("Найти собеседника не получилось ;6")

@dp.message_handler(state="connected")
async def _(message: types.Message, state: FSMContext):
    data = await state.get_data()
    buddy = data.get('buddy')
    name = data.get('name')
    txt = f"{name}: {message.text}"
    await bot.send_message(buddy, txt)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)