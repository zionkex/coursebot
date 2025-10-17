from aiogram import Router
from aiogram.types import CallbackQuery
from redis.asyncio import Redis
from keyboards.admin_inline import admin_panel_keyboard
from utils.buttons_enum import MenuButtons
from utils.callbacks import AdminCallback
from filters.isAdmin import isAdmin
from sqlalchemy.ext.asyncio import AsyncSession

admin_router = Router()

admin_router.message.register(isAdmin())


@admin_router.callback_query(AdminCallback.filter())
async def admin_callback(
    callback: CallbackQuery,
    callback_data: AdminCallback,
    session: AsyncSession,
    redis: Redis,
):
    if callback_data.action == MenuButtons.admin_panel.value.menu_name:
        text = (
            "👋 Вітаю в панелі адміністратора!\n"
            "Тут ви можете керувати системою та користувачами:\n"
            "🔹 Переглядати та редагувати список учнів і викладачів\n"
            "🔹 Створювати або редагувати курси та заняття\n"
            "🔹 Надсилати повідомлення або розсилки\n"
            "🔹 Керувати ролями та доступами \n "
            "Оберіть потрібну дію з меню нижче ⬇️"
        )
        kb = admin_panel_keyboard()
    await callback.message.edit_text(text=text, reply_markup=kb)
    await callback.answer()
