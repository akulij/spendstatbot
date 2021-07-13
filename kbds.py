from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

base_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

base_keyboard.row(KeyboardButton("Траты за неделю"), KeyboardButton("Траты за месяц"))
base_keyboard.row(KeyboardButton("Траты за год"), KeyboardButton("Траты семьи"))