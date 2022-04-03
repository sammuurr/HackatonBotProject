# coding=utf-8


from aiogram import Bot, Dispatcher, types

from data.project_settings import config

# init bot
bot = Bot(token=config["telegram_token"])


async def process_timetable_buttons(callback_query: types.CallbackQuery):
    # local important variables
    callback_query_data = callback_query.data

    # answer and say user about waiting
    await bot.answer_callback_query(callback_query.id, "Секундочку...")

    # update message to result
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=callback_query_data,
    )


# register all handlers
def register_handlers_timetable_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(
        process_timetable_buttons,
        lambda callback_data: callback_data.data and callback_data.data.startswith("timetable")
    )
