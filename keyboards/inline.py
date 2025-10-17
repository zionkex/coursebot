from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.buttons_enum import MenuButtons, StudentButtons
from aiogram.types import InlineKeyboardButton
from utils.callbacks import (
    MenuCallback,
    StudentCallback,
    TZCallback,
    AdminCallback,
    TeacherCallback,
)
# def main_keyboard() -> InlineKeyboardBuilder:
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Курси 📘", callback_data="view_courses")
#     builder.button(text="Мій профіль 👤", callback_data="view_profile")
#     builder.button(text="Розклад 🗓️", callback_data="view_schedule")
#     builder.button(text="Зворотній зв’язок 💬", callback_data="feedback")
#     builder.adjust(2)
#     return builder


def user_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Наші курси 📘", callback_data="view_courses")
    builder.adjust(2)
    return builder



def reminder_kb(url: str | None = None):
    kb = InlineKeyboardBuilder()
    if url:
        kb.button(text="Підключитись на урок", url=url)
    kb.button(
        text=MenuButtons.main_menu.value.text, callback_data=MenuCallback(action="main")
    )
    return kb.adjust(1).as_markup()


def timezone_kb(selected_button: int | None = None):
    kb = InlineKeyboardBuilder()
    for number in range(-10, 11):
        text = f"UTC {number:+}"
        if selected_button == text:
            text = f"✅{text}"
        kb.button(text=text, callback_data=TZCallback(zone=number, action=None))
        kb.adjust(5)
    kb.add(
        InlineKeyboardButton(
            text="Далі➡️", callback_data=TZCallback(action="next").pack()
        )
    )
    return kb.as_markup()


def admin_teacher_kb(teacher: bool = False, admin: bool = False):
    kb = InlineKeyboardBuilder()
    if teacher:
        kb.button(
            text=MenuButtons.teacher_panel.value.text,
            callback_data=TeacherCallback(
                action=MenuButtons.teacher_panel.value.menu_name
            ),
        )
    if admin:
        kb.button(
            text=MenuButtons.admin_panel.value.text,
            callback_data=AdminCallback(action=MenuButtons.admin_panel.value.menu_name),
        )
    return kb.adjust(1).as_markup()
