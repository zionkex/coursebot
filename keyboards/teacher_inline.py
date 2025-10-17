from database.models import Student
from utils.buttons_enum import StudentButtons, TeacherButtons
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.enums import TeacherEnum
from utils.callbacks import StudentCallback, TeacherCallback


def teacher_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for btn in [
        TeacherButtons.COURSES,
        TeacherButtons.STUDENTS,
        TeacherButtons.SCHEDULE,
        TeacherButtons.HOMEWORK,
    ]:
        builder.button(
            text=btn.text, callback_data=TeacherCallback(action=btn.menu_name, level=1)
        )
    builder.adjust(2)
    return builder.as_markup()


def teacher_students(students_info: list[Student], level: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for student in students_info:
        builder.button(
            text=student.user.telegram_name,
            callback_data=TeacherCallback(
                action=TeacherEnum.students_lesson.value, level=level + 1
            ),
        )
    return builder.adjust(1).as_markup()
