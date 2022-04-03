# coding=utf-8


import redis

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from project_services.help_redis import RedisHelper
from project_services.register_user import register_user


# init redis helper and redis client
redis_helper = RedisHelper()
redis_client = redis.Redis()


# register user state class
class Register(StatesGroup):
    waiting_for_full_name = State()


# register user
async def register_start(message: types.Message):
    # suggest entering full username
    messages_enter_name = ["Введи своё имя и фамилию.",
                           "Например: <b><i>Иван Иванов</i></b>"]

    await message.answer(messages_enter_name[0])
    await message.answer(messages_enter_name[1], parse_mode="html")

    # set waiting
    await Register.waiting_for_full_name.set()


# entering username
async def username_choosing(message: types.Message, state: FSMContext):
    # user
    user_id = message.from_user.id
    username = message.text.strip()

    # save in redis
    await redis_helper.redis_set("user_id", user_id)
    await redis_helper.redis_set("username", username)

    username_redis = redis_client.get("username")
    username_redis_decoded = await redis_helper.decode_bytes(username_redis)

    await register_user()

    await message.answer(f"Мы тебя запомнили, <b>{username_redis_decoded}</b>!", parse_mode="html")

    # close connection
    await redis_helper.close_storage()
    await state.finish()


# register all handlers
def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(register_start, state=None)
    dp.register_message_handler(username_choosing, state=Register.waiting_for_full_name)
