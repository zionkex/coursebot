import enum


class RoleEnum(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    USER = "user"
    PARENT = "parent"


class TeacherEnum(enum.Enum):
    students_lesson = "students_lesson"
