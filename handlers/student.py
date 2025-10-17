from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from aiogram import Router
from aiogram.types import CallbackQuery
from redis.asyncio import Redis
from database.queries import get_student_info, get_student_lessons, get_user_schedule

from keyboards.student_inline import student_keyboard
from redis_storages.user_cache import UserCache
from utils.callbacks import StudentCallback
from sqlalchemy.ext.asyncio import AsyncSession
from utils.buttons_enum import StudentButtons
from database.models import StudentLesson, UserSchedule
from utils.time import add_hours_to_time, change_time_to_user_zone
from config import settings

student_router = Router()


@student_router.callback_query(StudentCallback.filter())
async def student_handler(
    callback: CallbackQuery,
    callback_data: StudentCallback,
    session: AsyncSession,
    redis: Redis,
):
    user_cache = await UserCache.get(
        redis=redis, user_telegram_id=callback.from_user.id
    )
    if callback_data.action == StudentButtons.view_schedule.menu_name:
        user: UserCache = await UserCache.get(
            redis=redis, user_telegram_id=callback.from_user.id
        )
        data: list[UserSchedule] = await get_user_schedule(
            session=session, user_id=user.user_id
        )
        if data:
            days_with_emojis = [
                {"day": "Неділя", "emoji": "⚪"},
                {"day": "Понеділок", "emoji": "🔴"},
                {"day": "Вівторок", "emoji": "🟠"},
                {"day": "Середа", "emoji": "🟡"},
                {"day": "Четвер", "emoji": "🟢"},
                {"day": "П’ятниця", "emoji": "🔵"},
                {"day": "Субота", "emoji": "🟣"},
            ]

            text = "<b>Розклад уроків\n\n</b>"
            for schedule in data:
                day_info = days_with_emojis[schedule.day_of_week]
                student_time: datetime = change_time_to_user_zone(
                    utc_time=schedule.start_time, delta=user_cache.time_delta
                )
                text += (
                    f"<b>{day_info['emoji']}{day_info['day']}</b>\n"
                    f"<b>📘{schedule.course.title}</b>\n"
                    f"<b>⏰{student_time:%H:%M}-{student_time + timedelta(hours=1):%H:%M}</b>\n\n"
                )
            print(text)
            kb = student_keyboard(selected_button=StudentButtons.my_lessons)
            await callback.message.edit_text(text=text, reply_markup=kb)

        else:
            text = "У вас не має розкладу"
        kb = student_keyboard(selected_button=StudentButtons.view_schedule)
    elif callback_data.action == StudentButtons.my_lessons.menu_name:
        if user_cache.student_id:
            student_lessons: list[StudentLesson] = await get_student_lessons(
                session=session, student_id=user_cache.student_id, period=7
            )
            text = "Ваші уроки \n"
            for student_lesson in student_lessons:
                print(student_lesson.date)
                start_time = student_lesson.date + timedelta(
                    hours=user_cache.time_delta
                )
                print(user_cache.time_delta)
                end_time = start_time + timedelta(hours=1)
                text += (
                    f"<b>🔹Заняття:</b> {student_lesson.lesson.title}\n"
                    f"<b>🕐 Час:</b> {start_time:%H:%M} - {end_time:%H:%M}\n"
                    f"📝 <b>Д/З</b>: {student_lesson.homework}\n\n"
                )
        else:
            text = "Відсутні уроки"
        kb = student_keyboard(selected_button=StudentButtons.my_lessons)
    elif callback_data.action == StudentButtons.my_profile.menu_name:
        user_cache = await UserCache.get(
            redis=redis, user_telegram_id=callback.from_user.id
        )
        student_info = await get_student_info(
            session=session, student_id=user_cache.student_id
        )
        text = (
            "🎓 <b>Профіль студента</b>\n\n"
            f"‼️ <b>Залишилось: {student_info.paid - len(student_info.lessons)}</b>\n"
            f"💰 Оплачено уроків: {student_info.paid}\n"
            f"📘 Використано: {len(student_info.lessons)}\n"
        )
        kb = student_keyboard(selected_button=StudentButtons.my_profile)
    await callback.message.edit_text(text=text, reply_markup=kb)
    await callback.answer()
