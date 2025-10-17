from aiogram.filters import BaseFilter
from aiogram.types import Message
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from database.queries import get_admin
from redis_storages.user_cache import UserCache


class isTeacher(BaseFilter):
    async def __call__(self, message: Message, redis: Redis) -> bool:
        return not await UserCache.get(redis= redis, user_telegram_id=message.from_user.id)
