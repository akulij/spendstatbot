from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

base_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# base_keyboard.add(KeyboardButton("Создать лист покупок"))
# base_keyboard.add(KeyboardButton("Траты за день"))
base_keyboard.add(KeyboardButton("Траты за неделю"), KeyboardButton("Создать лист покупок"))
base_keyboard.add(KeyboardButton("Траты за месяц"), KeyboardButton("Траты семьи"))
# base_keyboard.add(KeyboardButton("Траты за все время"))
base_keyboard.add(KeyboardButton("Траты за год"), KeyboardButton("Статистика"))