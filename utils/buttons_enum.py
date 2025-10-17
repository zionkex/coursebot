from enum import Enum

from pydantic import BaseModel


class MenuItem(BaseModel):
    text: str
    menu_name: str


class MenuButtons(Enum):
    main_menu = MenuItem(text="Головне меню", menu_name="main_menu")
    teacher_panel = MenuItem(text="Панель вчителя", menu_name="teacher_panel")
    admin_panel = MenuItem(text="Панель адміна", menu_name="admin_panel")


class CustomEnum(Enum):
    @property
    def text(self) -> str:
        return self.value.text

    @property
    def menu_name(self) -> str:
        return self.value.menu_name


class StudentButtons(Enum):
    view_schedule = MenuItem(text="Розклад 🗓️", menu_name="view_schedule")
    my_profile = MenuItem(text="Мій профіль 👤", menu_name="view_profile")
    my_lessons = MenuItem(text="Мої уроки", menu_name="student_lessons")

    @property
    def text(self) -> str:
        return self.value.text

    @property
    def menu_name(self) -> str:
        return self.value.menu_name


class TeacherButtons(CustomEnum):
    COURSES = MenuItem(text="📚 Мої курси", menu_name="my_courses")
    STUDENTS = MenuItem(text="👩‍🎓 Студенти", menu_name="my_students")
    SCHEDULE = MenuItem(text="📅 Розклад", menu_name="schedule")
    HOMEWORK = MenuItem(text="📝 Домашні", menu_name="homework")

