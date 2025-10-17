from handlers.teacher import teacher_router
from handlers.user import user_router
from handlers.admin import admin_router
from handlers.student import student_router
from aiogram import Router

main_router = Router()
main_router.include_routers(user_router, student_router, teacher_router,admin_router)


__all__ = "main_router"
