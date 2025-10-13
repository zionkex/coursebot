from typing import Final, Self

import msgspec.msgpack
from redis.asyncio import Redis

# from storages.psql.utils.alchemy_struct import AlchemyStruct

ENCODER: Final[msgspec.msgpack.Encoder] = msgspec.msgpack.Encoder()


class UserCache(msgspec.Struct, kw_only=True):
    user_id: int
    student_id: int | None
    teacher_id: int | None
    admin_id: int | None
    # role: str

    @classmethod
    def key(cls, user_telegram_id: int | str) -> str:
        return f"{cls.__name__}:{user_telegram_id}"

    async def save(self, redis: Redis, user_telegram_id: int | str) -> None:
        key = self.key(user_telegram_id)
        await redis.set(key, ENCODER.encode(self))

    @classmethod
    async def get(cls, redis: Redis, user_telegram_id: int | str) -> Self | None:
        data = await redis.get(cls.key(user_telegram_id))
        if data is None:
            return None
        return msgspec.msgpack.decode(data, type=cls)

    @classmethod
    async def delete(cls, redis: Redis, user_telegram_id: int | str) -> int:
        return await redis.delete(cls.key(user_telegram_id))

    @classmethod
    async def delete_all(cls, redis: Redis) -> int:
        keys = await redis.keys(f"{cls.__name__}:*")
        return await redis.delete(*keys) if keys else 0
