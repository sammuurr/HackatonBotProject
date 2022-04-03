# coding=utf-8


import redis

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from project_services.help_redis import RedisHelper
from project_services.generate_token import generate_token


# init redis helper and redis client
redis_helper = RedisHelper()
redis_client = redis.Redis()


# register user state class
class CreateGroup(StatesGroup):
    waiting_for_group_name = State()
    waiting_for_subject = State()


# register user
async def register_start(message: types.Message):
    # suggest entering full username
    messages_enter_group_name = ["Введи имя своей группы.",
                                 "Например: <b><i>9 класс учеба</i></b>"]

    await message.answer(messages_enter_group_name[0])
    await message.answer(messages_enter_group_name[1], parse_mode="html")

    # set waiting
    await CreateGroup.waiting_for_group_name.set()


# entering username
async def group_name_choosing(message: types.Message):
    # user
    admin_id = message.from_user.id
    group_name = message.text.strip()

    # save in redis
    await redis_helper.redis_set("admin_id", admin_id)
    await redis_helper.redis_set("group_name", group_name)

    await message.answer(f"Теперь введите предмет, например, <b><i>Математика</i></b>")

    await CreateGroup.next()


async def subject_choosing(message: types.Message, state: FSMContext):
    subject = message.text
    token = generate_token()

    await redis_helper.redis_set("subject", subject)
    await redis_helper.redis_set("token", token)

    group_name_redis = redis_client.get("group_name")
    group_name_redis_decoded = await redis_helper.decode_bytes(group_name_redis)

    token_redis = redis_client.get("token")
    token_redis_decoded = await redis_helper.decode_bytes(token_redis)

    admin_id_redis = redis_client.get("admin_id")
    admin_id_redis_decoded = await redis_helper.decode_bytes(admin_id_redis)

    await message.answer(f"Мы запомнили твою группу: <b>{group_name_redis_decoded}</b>!", parse_mode="html")
    await message.answer(f"Информация о группе:\n\n<b>id админа группы</b>: {admin_id_redis_decoded}"
                         f"\n<b>Токен для доступа в группу</b>: {token_redis_decoded}")

    redis_client.close()
    await redis_helper.close_storage()
    await state.finish()


# register all handlers
def register_handlers_create_group(dp: Dispatcher):
    dp.register_message_handler(register_start, commands=["create_group"], state=None)
    dp.register_message_handler(group_name_choosing, state=CreateGroup.waiting_for_group_name)
    dp.register_message_handler(subject_choosing, state=CreateGroup.waiting_for_subject)
