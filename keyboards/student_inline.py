from utils.buttons_enum import StudentButtons
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbacks import StudentCallback

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
