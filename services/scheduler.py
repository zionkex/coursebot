import asyncio
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo
import msgspec
from redis.asyncio import Redis
from aiogram import Bot

from utils.time import TimeEnum


class Reminder(msgspec.Struct, kw_only=True):
    user_id: int
    interval_days: int = 7
    time: TimeEnum


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
        print(
            f"Нагадування буде відправлено в {next_reminder.astimezone(ZoneInfo('Europe/Kyiv'))}"
        )
        await self.redis.zadd(self.redis_key, {data: next_reminder.timestamp()})

    async def send_before_lesson_reminder(self, reminder: Reminder):
        await self.bot.send_message(chat_id=reminder.user_id)

    async def _process_due_reminders(self):
        while True:
            now_ts = datetime.now(timezone.utc).timestamp()
            reminders = await self.redis.zrangebyscore(self.redis_key, 0, now_ts)
            for data in reminders:
                reminder = msgspec.msgpack.decode(data, type=Reminder)
                self.send_before_lesson_reminder(reminder=reminder)
                await self.redis.zrem(self.redis_key, data)
            await asyncio.sleep(1)

    async def start(self):
        if self.loop_task is None:
            self.loop_task = asyncio.create_task(self._process_due_reminders())

    async def stop(self):
        if self.loop_task:
            self.loop_task.cancel()
            self.loop_task = None
