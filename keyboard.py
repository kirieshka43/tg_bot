from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup, ForceReply
from aiogram import types


new_cart_bt = KeyboardButton("Cоздать новый список")
connect_cart_bt = KeyboardButton("Найти список")

cart_kb = ReplyKeyboardMarkup(one_time_keyboard=False).add(new_cart_bt, connect_cart_bt)

add_item_bt = KeyboardButton("Добавить элемент")
remove_item_bt = KeyboardButton("Удалить элемент")
show_item_bt = KeyboardButton("Показать список")

item_kb = ReplyKeyboardMarkup(one_time_keyboard=False).add(add_item_bt, remove_item_bt).add(show_item_bt)