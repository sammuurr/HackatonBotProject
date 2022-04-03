# coding=utf-8


from aiogram import Dispatcher, types

from keyboards.reply_keyboards.start_keyboard import *


# process start command
async def process_start_command(message: types.Message):
    # init local variables
    user_name = message.from_user.full_name
    hello_message_text = f"Привет, {user_name} :) Нажми на кнопочку"

    # send start message
    await message.answer(text=hello_message_text, reply_markup=start_keyboard)


# register all handlers
def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=["start", "help", "begin"])
