from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.queries import get_admin


class isAdmin(BaseFilter):
    is_admin: bool = True

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        admin = await get_admin(session=session, telegram_id=message.from_user.id)
        return bool(admin) == self.is_admin
