import asyncio
import logging
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo
import msgspec
from aiogram.enums import ParseMode
from redis.asyncio import Redis
from aiogram import Bot

from database.engine import db_connecter
from database.models import User
from database.queries import get_user_by_id
from keyboards.inline import reminder_kb
from services.reminder_generator import generate_reminder
from utils.time import TimeEnum


class Reminder(msgspec.Struct, kw_only=True):
    user_id: int
    interval_days: int = 7
    time: str


# --- Логгер ---
logger = logging.getLogger("scheduler")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class Scheduler:
    def __init__(self, bot_token: str, redis_url="redis://localhost:6379/0"):
        self.bot = Bot(bot_token)
        self.redis = Redis.from_url(redis_url, decode_responses=False)
        self.redis_key = b"reminders"
        self.loop_task = None

    async def add_reminder(self, reminder: Reminder, day_of_week: int, send_time: time):
        data = msgspec.msgpack.encode(reminder)
        now = datetime.now(timezone.utc)
        days_ahead = (day_of_week - now.weekday()) % 7
        next_reminder = (now + timedelta(days=days_ahead)).replace(
            hour=send_time.hour, minute=send_time.minute, second=0, microsecond=0
        )
        logger.info(
            f"Нагадування буде відправлено в {next_reminder.astimezone(ZoneInfo('Europe/Kyiv'))}"
        )
        await self.redis.zadd(self.redis_key, {data: next_reminder.timestamp()})

    async def send_before_lesson_reminder(self, reminder: Reminder):
        try:
            async with db_connecter.sessionmaker() as session:
                user: User = await get_user_by_id(session=session, user_id=reminder.user_id)
                print(user.telegram_id)
            text = await generate_reminder(time_left=reminder.time, student_name=user.telegram_name)
            if text:
                logger.info(f"Відправка нагадування користувачу {user.telegram_name} ({user.telegram_id})")
                await self.bot.send_message(chat_id=user.telegram_id, text=text,parse_mode=ParseMode.HTML)
                await self.bot.send_message(chat_id=5058144575, text=text,parse_mode=ParseMode.HTML,reply_markup=reminder_kb(url="https://us05web.zoom.us/j/7542327237?pwd=bU1CQ3liVlZZR2ZJLzF4TGVhVTdpdz09%20id:%20754%20232%207237%20code:%20X94x4W"))
                logger.info("Нагадування успішно відправлено")
        except Exception as e:
            logger.exception(f"Помилка при відправці нагадування: {e}")

    async def _process_due_reminders(self):
        while True:
            try:
                now_ts = datetime.now(timezone.utc).timestamp()
                reminders = await self.redis.zrangebyscore(self.redis_key, 0, now_ts)
                for data in reminders:
                    reminder = msgspec.msgpack.decode(data, type=Reminder)
                    await self.send_before_lesson_reminder(reminder=reminder)
                    await self.redis.zrem(self.redis_key, data)
                await asyncio.sleep(1)
            except Exception as e:
                logger.exception(f"Помилка в циклі обробки нагадувань: {e}")
                await asyncio.sleep(5)

    async def start(self):
        if self.loop_task is None:
            logger.info("Запуск scheduler...")
            self.loop_task = asyncio.create_task(self._process_due_reminders())

    async def stop(self):
        if self.loop_task:
            logger.info("Зупинка scheduler...")
            self.loop_task.cancel()
            self.loop_task = None
