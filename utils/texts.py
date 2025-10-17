from datetime import datetime, timezone
from database.models import User
from keyboards.inline import admin_teacher_kb, timezone_kb
from keyboards.student_inline import student_keyboard
from redis_storages.user_cache import UserCache
from utils.enums import RoleEnum


def is_regular_user(user: UserCache) -> bool:
    return user.student_id is None and user.teacher_id is None and user.admin_id is None


def start_text(user: UserCache, full_name: str):
    text = f"🎓 Вітаю, <b>{full_name}</b>!\nРадий бачити тебе в нашому навчальному боті 👋 🚀"
    if not user or is_regular_user(user=user):
        text = (
            f"Привіт <b>{full_name}</b>! 👋 Я — твій помічник у програмуванні, Пітончик 🐍💡\n\n"
            "Готовий разом вчитися, грати та розвивати свої навички?\n"
            "Давай почнемо! 🚀"
        )
        kb = None
    elif user.is_admin_and_teacher():
        text = "Виберіть, яка сама панель вам потрібна"
        kb = admin_teacher_kb(teacher=True, admin=True)
    elif user.is_student():
        kb = student_keyboard()
    elif user.is_admin():
        kb = None

    elif user.is_teacher():
        kb = None
    return text, kb


def get_user_time_zone():
    utc_now = datetime.now(timezone.utc).time()
    text = (
        "Для зручного користування ботом просимо вибрати Ваш часовий пояс.\n"
        f"Для визначення часового поясу віднміть від вашого часу <b>{utc_now}</b>, різниця і буде ваш часовий пояс\n"
        "Нижче виберіть Ваш часовий пояс"
    )
    kb = timezone_kb()
    return text, kb
