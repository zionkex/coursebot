from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from database.models import User
from database.queries import add_user, get_user_by_telegram_id
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.inline import student_keyboard
from utils.role_enums import RoleEnum
from utils.texts import start_text

user_router = Router()


@user_router.message(CommandStart())
async def command_start(message: Message, session: AsyncSession):
    user: User = await get_user_by_telegram_id(
        session=session, telegram_id=message.from_user.id, get_roles=True
    )
    if not user:
        await add_user(
            session,
            message.from_user.id,
            message.from_user.full_name,
            message.from_user.username,
        )
    text, kb = start_text(user, message.from_user.full_name)

    await message.answer(text, reply_markup=kb)
