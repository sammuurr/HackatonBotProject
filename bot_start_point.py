# coding=utf-8


import logging

from aiogram import Bot, Dispatcher, executor

from data.project_settings import config
from project_services.help_redis import RedisHelper
from handlers.data_handlers import timetable_buttons_handler
from handlers.command_text_handlers import start_handler, text_handler, register_handler  #, register_group_handler


# logging info
logging.basicConfig(level=logging.INFO)

# init tokens
telegram_token = str(config["telegram_token"])

# init redis helper and redis storage
redis_helper = RedisHelper()
redis_storage = redis_helper.redis_storage

# init bot and dispatcher
bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=redis_storage)


# register command and text handlers
register_handler.register_handlers_register(dp)
start_handler.register_handlers_start(dp)  # register 'start' command handler
text_handler.register_handlers_text(dp)

# register callback data handlers
timetable_buttons_handler.register_handlers_timetable_buttons(dp)  # register timetable buttons


if __name__ == "__main__":
    executor.start_polling(dp)
