from datetime import time
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.redis import RedisJobStore
from config import settings
from database.engine import db_connecter
from database.queries import get_user_and_teacher_url_by_schedule
from keyboards.inline import reminder_kb
from testAI import generate_reminder, TimeEnum


jobstore = RedisJobStore(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    db=0,
)
scheduler = AsyncIOScheduler()
scheduler.add_jobstore(jobstore, "default")

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def remind_before_lesson(schedule_id: int, reminder_type: str, bot: Bot = bot):
    async with db_connecter.sessionmaker() as session:
        (
            user_telegram_id,
            telegram_name,
            teacher_url,
        ) = await get_user_and_teacher_url_by_schedule(
            session=session, schedule_id=schedule_id
        )
        if reminder_type == "2h":
            text = await generate_reminder(
                student_name=telegram_name, time_left=TimeEnum.two_hour
            )
            kb = None
        else:
            text = await generate_reminder(
                student_name=telegram_name, time_left=TimeEnum.fifteen_minutes
            )
            kb = reminder_kb(teacher_url)
        # text = await two_hour_reminder_text(student_name="Давид")
    await bot.send_message(chat_id=user_telegram_id, text=text, reply_markup=kb)
    pass


def add_reminder_job(
    schedule_id: int, day_of_week: int, lesson_time: time, reminder_type: str
):
    scheduler.add_job(
        remind_before_lesson,
        CronTrigger(
            day_of_week=day_of_week, hour=lesson_time.hour, minute=lesson_time.minute
        ),
        id=f"job_{reminder_type}_{schedule_id}",
        replace_existing=True,
        args=[schedule_id, reminder_type],
    )


# def add_tets():
#     scheduler.add_job(
#         remind_two_hours_before_lesson,
#         CronTrigger(minute="*/1"),
#         id="job11",
#         replace_existing=True,
#     )
