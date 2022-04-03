# coding=utf-8


import redis

from project_services.help_redis import RedisHelper
from project_services.database_controller import DatabaseController


redis_client = redis.Redis()
redis_helper = RedisHelper()
database_controller = DatabaseController()


async def register_user():
    username_encoded = redis_client.get("username")
    user_id_encoded = redis_client.get("user_id")

    username_decoded = await redis_helper.decode_bytes(username_encoded)
    user_id_decoded = await redis_helper.decode_bytes(user_id_encoded)

    save_user_query = f"INSERT INTO users (user_id, user_full_name) VALUES " \
                      f"('{user_id_decoded}', '{username_decoded}')"

    database_controller.execute_query(save_user_query)

    await redis_helper.close_storage()
