from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.buttons_enum import MenuButtons, StudentButtons
from utils.callbacks import MenuCallback, StudentCallback
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


def student_keyboard(selected_button=None) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for btn in [
        StudentButtons.my_profile,
        StudentButtons.view_schedule,
        StudentButtons.my_lessons,
    ]:
        text = f"✅{btn.text}" if btn == selected_button else btn.text
        builder.button(
            text=text, callback_data=StudentCallback(action=btn.menu_name, level=0)
        )
    builder.adjust(2)
    return builder.as_markup()


def reminder_kb(url: str | None = None):
    kb = InlineKeyboardBuilder()
    if url:
        kb.button(text="Підключитись на урок", url=url)
    kb.button(
        text=MenuButtons.main_menu.value, callback_data=MenuCallback(action="main")
    )
    return kb.as_markup(1)
