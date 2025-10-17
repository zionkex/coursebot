from aiogram.filters.callback_data import CallbackData


class BaseCallback(CallbackData, prefix="base"):
    action: str
    level: int = 0


class UserCallback(BaseCallback, prefix="user"):
    pass


class AdminCallback(BaseCallback, prefix="admin"):
    pass


class TeacherCallback(BaseCallback, prefix="teacher"):
    pass


class StudentCallback(BaseCallback, prefix="student"):
    pass


class MenuCallback(BaseCallback, prefix="menu"):
    pass


class TZCallback(CallbackData, prefix="TZ"):
    zone: int | None = None
    action: str | None = None
