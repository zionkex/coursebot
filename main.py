import asyncio
import sys
from aiogram import Bot, Dispatcher
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from config import settings
from middlewares.session import DataBaseSession
from database.engine import db_connecter
from services.scheduler import add_all_scheduler, add_reminder_job, scheduler
from handlers import main_router

dp = Dispatcher(
    storage=RedisStorage.from_url(
        url=settings.redis.url,
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )
)
dp.update.middleware(DataBaseSession(db_connecter.sessionmaker))
dp.include_router(main_router)


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    scheduler.start()
    scheduler.remove_all_jobs()
    # add_reminder_job(schedule_id=1, day_of_week=1, lesson_time=1, reminder_type="15m")
    # add_reminder_job()
    # scheduler.ctx.add_instance(bot, declared_class=Bot)
    await add_all_scheduler(1)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
