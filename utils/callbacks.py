from aiogram.filters.callback_data import CallbackData


class BaseCallback(CallbackData, prefix="base"):
    action: str
    level: int = 0


class UserCallback(BaseCallback, prefix="user"):
    pass


class AdminCallback(BaseCallback, prefix="admin"):
    pass


class StudentCallback(BaseCallback, prefix="student"):
    pass


class MenuCallback(BaseCallback, prefix="menu"):
    pass
