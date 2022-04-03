# coding=utf-8


import redis

from project_services.help_redis import RedisHelper
from project_services.generate_token import generate_token
from project_services.database_controller import DatabaseController


redis_client = redis.Redis()
redis_helper = RedisHelper()
database_controller = DatabaseController()


async def register_group():
    token = generate_token()
    await redis_helper.redis_set("token", token)

    await redis_helper.close_storage()
