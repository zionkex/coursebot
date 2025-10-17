from aiogram import Router
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

from database.queries import get_teacher_enrollments_with_student
from filters.teacher import isTeacher
from keyboards.admin_inline import admin_panel_keyboard
from keyboards.teacher_inline import teacher_keyboard, teacher_students
from redis_storages.user_cache import UserCache
from utils.buttons_enum import MenuButtons, TeacherButtons
from utils.callbacks import AdminCallback, TeacherCallback
from filters.isAdmin import isAdmin
from sqlalchemy.ext.asyncio import AsyncSession

teacher_router = Router()

teacher_router.message.register(isTeacher())


@teacher_router.callback_query(TeacherCallback.filter())
async def teacher_callback(
    callback: CallbackQuery,
    callback_data: AdminCallback,
    session: AsyncSession,
    redis: Redis,
):
    usercache: UserCache = await UserCache.get(
        redis=redis, user_telegram_id=callback.from_user.id
    )
    if callback_data.action == MenuButtons.teacher_panel.value.menu_name:
        text = (
            f"👋 <b>Вітаю, {callback.from_user.full_name}!</b>\n\n"
            "Це <b>панель вчителя</b> — ваш персональний помічник для управління курсами, "
            "студентами та розкладом.\n\n"
            "Ви можете:\n"
        )
        kb = teacher_keyboard()
    elif callback_data.level == 1:
        if callback_data.action == TeacherButtons.STUDENTS.menu_name:
            enrollments = await get_teacher_enrollments_with_student(
                session=session, teacher_id=usercache.teacher_id
            )
            if enrollments:
                text = "<b>Ваші учні</b>"
                students_info = [enrollment.student for enrollment in enrollments]
                kb = teacher_students(
                    students_info=students_info, level=callback_data.level
                )
            else:
                text = "У вас ще не має учнів"
                kb = None   
    await callback.message.edit_text(text=text, reply_markup=kb)
    await callback.answer()
