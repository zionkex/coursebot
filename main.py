import asyncio
import sys
from datetime import time

from aiogram import Bot, Dispatcher
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio import Redis
from config import settings
from middlewares.redis import RedisConnection
from middlewares.session import DataBaseSession
from database.engine import db_connecter
from services.scheduler import Reminder, Scheduler
from handlers import main_router
from utils.time import TimeEnum

dp = Dispatcher(
    storage=RedisStorage.from_url(
        url=settings.redis.url,
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )
)
dp.update.middleware(DataBaseSession(db_connecter.sessionmaker))
dp.update.middleware(RedisConnection(Redis.from_url(url=settings.redis.url)))
dp.include_router(main_router)


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    scheduler = Scheduler(redis_url=settings.redis.url, bot_token=settings.BOT_TOKEN)
    await scheduler.start()
    reminder = Reminder(user_id=1,interval_days=7,time=TimeEnum.value)
    await scheduler.add_reminder(reminder=reminder,day_of_week=4,send_time=time(14,45))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
