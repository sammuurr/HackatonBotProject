# coding=utf-8


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# init timetable keyboard
timetable_keyboard = InlineKeyboardMarkup()

# init buttons
get_timetable_button = InlineKeyboardButton("Получить расписание", callback_data="timetable_get_timetable")

# join buttons
timetable_keyboard.add(get_timetable_button)
