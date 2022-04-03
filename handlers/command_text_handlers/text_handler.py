# coding=utf-8


from aiogram import Bot, types, Dispatcher

from data.project_settings import config
from project_services.database_controller import DatabaseController


# get telegram token
telegram_token = config["telegram_token"]  # telegram token

# init bot
bot = Bot(token=telegram_token)

# init database controller
database_controller = DatabaseController()


# process usual text
async def usual_text(message: types.Message):
    # local variables
    user_request = message.text.lower()

    # process text
    if user_request == "создать группу ✍️":
        # user's id
        user_id = message.from_user.id

        # get user in db
        search_user_query = f"SELECT * FROM users WHERE user_id='{user_id}'"  # query for searching user in db
        found_user = database_controller.get_data_execute_query(search_user_query)

        # check if user in db
        if len(found_user) == 0:
            register_messages = ["Ты не зарегистрирован :(",
                                 "<b>Нажми на меня</b>, чтобы зарегистрироваться /register"]  # mes

            await message.answer(register_messages[0])  # not registered notification
            await message.answer(register_messages[1], parse_mode="html")  # suggest to register
        # else:
        #     create_group_message = "<b>Нажми на меня</b>, чтобы её создать /сreate_group"  # mes
        #
        #     await message.answer(create_group_message, parse_mode="html")
    elif user_request == "Вступить в группу 🔗":
        await message.answer("<b>Пока</b> что не доступно, но скоро будет :)")


# register all handlers
def register_handlers_text(dp: Dispatcher):
    dp.register_message_handler(usual_text, content_types=types.ContentTypes.TEXT)
