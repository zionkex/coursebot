from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from redis.asyncio import Redis

from database.models import User
from database.queries import add_user, get_user_by_telegram_id
from sqlalchemy.ext.asyncio import AsyncSession
from redis_storages.user_cache import UserCache
from utils.enums import RoleEnum
from utils.texts import get_user_time_zone, start_text

user_router = Router()


def is_regular_user(user: UserCache) -> bool:
    return user.student_id is None and user.teacher_id is None and user.admin_id is None


@user_router.message(CommandStart())
async def command_start(message: Message, session: AsyncSession, redis: Redis):
    user: User = await get_user_by_telegram_id(
        session=session, telegram_id=message.from_user.id, get_roles=True
    )
    if not user:
        new_user = await add_user(
            session,
            message.from_user.id,
            message.from_user.full_name,
            message.from_user.username,
        )
        user_to_redis = UserCache(user_id=new_user.id)
        await user_to_redis.save(
            redis=redis,
            user_telegram_id=message.from_user.id,
        )
    # elif not user.timedelta:
    else:
        user = await UserCache.get(redis=redis, user_telegram_id=user.telegram_id)
        text, kb = start_text(user, message.from_user.full_name)
    # text, kb = get_user_time_zone()

    await message.answer(text, reply_markup=kb)
