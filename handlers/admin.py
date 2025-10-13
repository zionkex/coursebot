from aiogram import Router
from aiogram.types import Message
from keyboards.admin_inline import admin_panel_keyboard
from utils.isAdmin import isAdmin


admin_router = Router()

admin_router.message.register(isAdmin())


@admin_router.message()
async def admin_panel(message: Message):
    await message.answer(
        "Вітаю в адмін-панелі! Тут ти можеш керувати ботом.",
        reply_markup=admin_panel_keyboard(),
    )
