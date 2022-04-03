# coding=utf-8


import redis
from aiogram.contrib.fsm_storage.redis import RedisStorage2


class RedisHelper:
    def __init__(self):
        # create redis connection
        try:
            self.redis_client = redis.Redis()  # create redis client
        except redis.exceptions as redis_error:
            print(f"[redis] some error has occurred: {redis_error}")
        finally:
            self.redis_client.close()  # close redis connection if we got some exception

        self.redis_storage = RedisStorage2(
            host="localhost", port=6379, db=0
        )

    @staticmethod
    async def decode_bytes(encoded_value):
        """
        :param encoded_value: data to decode
        :return: gets redis byte data and return decoded data
        """

        return encoded_value.decode("utf-8")

    async def redis_set(self, name, value):
        """
        :param name: key name
        :param value: key value
        :return: bool, creates a note with key data on redis server
        """

        return self.redis_client.set(name=name, value=value)

    async def close_storage(self):
        """
        :return: closes redis storage and clear data
        """

        await self.redis_storage.close()
        await self.redis_storage.wait_closed()
