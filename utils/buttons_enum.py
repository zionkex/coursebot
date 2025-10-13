from enum import Enum

from pydantic import BaseModel


class MenuItem(BaseModel):
    text: str
    menu_name: str


class MenuButtons(Enum):
    main_menu = MenuItem(text="Головне меню", menu_name="main_menu")


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
