from aiogram import Router
from aiogram.types import CallbackQuery
from redis.asyncio import Redis
from database.queries import get_student_lessons, get_user_schedule
from keyboards.inline import student_keyboard
from redis_storages.user_cache import UserCache
from utils.callbacks import StudentCallback
from sqlalchemy.ext.asyncio import AsyncSession
from utils.buttons_enum import StudentButtons
from database.models import StudentLesson, UserSchedule
from utils.time import add_hours_to_time
from config import settings

student_router = Router()


@student_router.callback_query(StudentCallback.filter())
async def student_handler(
    callback: CallbackQuery, callback_data: StudentCallback, session: AsyncSession
):
    redis = Redis.from_url(
        f"redis://:{settings.redis.password}@{settings.redis.host}:6379/0"
    )
    if callback_data.action == StudentButtons.view_schedule.menu_name:
        user_id = await UserCache.get(
            redis=redis, user_telegram_id=callback.from_user.id
        )
        print(user_id, type(user_id), "-*")
        data: UserSchedule = await get_user_schedule(session=session, user_id=user_id)
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
                text += (
                    f"<b>{day_info['emoji']}{day_info['day']}</b>\n"
                    f"<b>📘{schedule.course.title}<b>\n"
                    f"<b>⏰{schedule.start_time.strftime('%H:%M')}-{add_hours_to_time(schedule.start_time).strftime('%H:%M')}</b>\n\n"
                )
            print(text)

        else:
            text = "У вас не має розкладу"
        kb = student_keyboard(selected_button=StudentButtons.view_schedule)
    if callback_data.action == StudentButtons.my_lessons:
        user_ids = await UserCache.get(
            redis=redis, user_telegram_id=callback.from_user.id
        )
        if user_ids.student_id:
            student_lessons: list[StudentLesson] = await get_student_lessons(
                session=session, student_id=user_ids.student_id
            )
            text = ""
            for student_lesson in student_lessons:
                text += (
                    f"<b>🔹Заняття:</b> {student_lesson.lesson.title}\n"
                    f"<b🕐Час</b> {student_lesson.date.time()} - {add_hours_to_time(student_lesson.date.time(), hours=1)}\n"
                    f"📝 <b>Д/З</b>: {student_lesson.homework}\n\n"
                )
        else:
            text = "Відсутні уроки"
        kb = student_keyboard(selected_button=StudentButtons.my_lessons)
    await callback.message.edit_text(text=text, reply_markup=kb)
