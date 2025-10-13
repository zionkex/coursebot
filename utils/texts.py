from database.models import User
from keyboards.inline import student_keyboard
from utils.role_enums import RoleEnum


def start_text(user: User, full_name: str):
    text = f"🎓 Вітаю, <b>{full_name}</b>!\nРадий бачити тебе в нашому навчальному боті 👋 🚀"
    if not user or any(RoleEnum.USER.value == role.name for role in user.roles):
        text = (
            f"Привіт <b>{full_name}</b>! 👋 Я — твій помічник у програмуванні, Пітончик 🐍💡\n\n"
            "Готовий разом вчитися, грати та розвивати свої навички?\n"
            "Давай почнемо! 🚀"
        )
        kb = None
    elif any(RoleEnum.STUDENT.value == role.name for role in user.roles):
        kb = student_keyboard()
    elif any(RoleEnum.TEACHER.value == role.name for role in user.roles):
        kb = None

    elif any(RoleEnum.ADMIN.value == role.name for role in user.roles):
        kb = None
    return text, kb
