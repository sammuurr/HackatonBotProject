# coding=utf-8


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# init start keyboard
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# init start buttons
create_group_button = KeyboardButton("Создать группу ✍️")
join_group_button = KeyboardButton("Вступить в группу 🔗")


# join buttons
start_keyboard.add(create_group_button, join_group_button)
