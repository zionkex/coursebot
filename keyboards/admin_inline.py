from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbacks import AdminCallback
from utils.buttons_enum import MenuItem

ADMIN_BUTTONS: list[MenuItem] = [
    MenuItem(text="Студенти 🎓", menu_name="manage_students"),
    MenuItem(text="Викладачі 👨‍🏫", menu_name="manage_teachers"),
    MenuItem(text="Курси 📘", menu_name="manage_courses"),
    MenuItem(text="Уроки 🧾", menu_name="manage_lessons"),
    MenuItem(text="Розклад 🗓️", menu_name="manage_schedule"),
    MenuItem(text="Розсилки 📢", menu_name="mailings"),
    MenuItem(text="Зворотній зв’язок 💬", menu_name="feedback"),
    MenuItem(text="Статистика 📈", menu_name="statistics"),
    MenuItem(text="Налаштування ⚙️", menu_name="settings"),
]


def admin_panel_keyboard(row_width: int = 3) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for btn in ADMIN_BUTTONS:
        builder.button(
            text=btn.text,
            callback_data=AdminCallback(action=btn.callback_data, level=0),
        )
    builder.adjust(row_width)
    return builder
