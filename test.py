import asyncio
from datetime import timedelta
from zoneinfo import ZoneInfo

from database.engine import DatabaseConnecter
from config import settings
from database.models import User, UserSchedule
from database.queries import (
    get_all_users,
    get_student_lessons,
    get_teacher_enrollments_with_student_and,
    get_user_schedule,
)
from redis_storages.user_cache import UserCache
from redis.asyncio import Redis

from utils.time import add_hours_to_time

db2 = DatabaseConnecter(
    url=f"postgresql+asyncpg://{settings.db.postgres_user}:{settings.db.postgres_password}@localhost:5435/{settings.db.postgres_db}",
    echo=settings.db.echo,
    max_overflow=settings.db.max_overflow,
)

redis = Redis.from_url(f"redis://:{settings.redis.password}@localhost:6379/0")


async def main():
    async with db2.sessionmaker() as session:
        data = await get_teacher_enrollments_with_student_and(
            session=session, teacher_id=1
        )
        for dat in data:
            print(dat.student.user.telegram_name)
    # print(await redis.keys("*"))
    # schedules = await get_user_schedule(session=session, user_id=1)
    # for schedule in schedules:
    #     print(schedule.start_time - timedelta(2))
    # data = await get_user_schedule(session=session, user_id=1)
    # for i in data:
    #     print(i.course.title)
    # await UserCache.delete_all(redis)
    # data: list[User] = await get_all_users(session=session, all_profiles=True)
    # for user in data:
    # print(user)
    # await UserCache.delete_all(redis=redis)
    # if user.student_profile:
    #     print(user.student_profile.id)
    # if user.teacher_profile:
    #     print(user.teacher_profile.id)
    # if user.admin_profile:
    #     print(user.admin_profile.id)
    # print("_______________")
    # user_to_redis = UserCache(
    #     user_id=user.id,
    #     student_id=user.student_profile.id if user.student_profile else None,
    #     teacher_id=user.teacher_profile.id if user.teacher_profile else None,
    #     admin_id=user.admin_profile.id if user.admin_profile else None,
    #     time_delta=user.timedelta,
    # )
    # user_to_redis.delete_all(redis=redis)
    # user_to_redis = UserCache(id=user.telegram_id, value=user.id)
    #     await user_to_redis.save(redis=redis, user_telegram_id=user.telegram_id)
    #     user_data = await UserCache.get(
    #         redis=redis, user_telegram_id=user.telegram_id
    #     )
    #     print(user_data)
    # # print(user_data)
    # print(user.telegram_id, "->", user_data)


asyncio.run(main())
# from database.queries import get_user_schedule


# async def main():
#     async with db2.sessionmaker() as session:
#         data: UserSchedule = await get_user_schedule(session=session, user_id=1)
#         # await UserID.delete_all(redis)
#         if data:
#             days_with_emojis = [
#                 {"day": "Неділя", "emoji": "⚪"},
#                 {"day": "Понеділок", "emoji": "🔴"},
#                 {"day": "Вівторок", "emoji": "🟠"},
#                 {"day": "Середа", "emoji": "🟡"},
#                 {"day": "Четвер", "emoji": "🟢"},
#                 {"day": "П’ятниця", "emoji": "🔵"},
#                 {"day": "Субота", "emoji": "🟣"},
#             ]

#             # for i in data:
#             #     print(i.course.title)
#             # text = "Розклад"
#             text = "Розклад уроків\n\n"
#             for schedule in data:
#                 day_info = days_with_emojis[schedule.day_of_week]
#                 text += (
#                     f"<b>{day_info['emoji']}{day_info['day']}</b>\n"
#                     f"<b>📘{schedule.course.title}<b>\n"
#                     f"<b>⏰{schedule.start_time.strftime('%H:%M')}-{add_hours_to_time(schedule.start_time).strftime('%H:%M')}</b>\n\n"
#                 )
#             print(text)


# asyncio.run(main())
