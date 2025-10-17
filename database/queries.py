from datetime import datetime, time, timedelta
from typing import Tuple
from database.models import (
    Admin,
    Course,
    Enrollment,
    Lesson,
    Role,
    Student,
    StudentLesson,
    Teacher,
)
from database.models import UserSchedule
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from sqlalchemy.orm import selectinload, joinedload
from database.models import User
from utils.enums import RoleEnum


async def add_user(
    session: AsyncSession, telegram_id: int, telegram_name: str, telegram_username: str
) -> int:
    new_user = User(
        telegram_id=telegram_id,
        telegram_name=telegram_name,
        telegram_username=telegram_username,
    )
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user.id
    except:
        await session.rollback()


async def add_profile(
    session: AsyncSession,
    user_id: int,
    model: type[Student] | type[Teacher] | type[Admin],
):
    profile = model(user_id=user_id)
    session.add(profile)
    await session.commit()


async def add_enrollment(
    session: AsyncSession, student_id: int, course_id: int, teacher_id: int
):
    enrollment = Enrollment(
        student_id=student_id, course_id=course_id, teacher_id=teacher_id
    )
    session.add(enrollment)
    await session.commit()


async def add_role_for_user(
    session: AsyncSession, telegram_id: int, role_name: RoleEnum, get_roles: bool = True
) -> User:
    user = await get_user_by_telegram_id(session, telegram_id, get_roles)
    role = await get_role_by_name(session, role_name.value)
    if user and role not in user.roles:
        user.roles.append(role)
    session.add(user)
    await session.commit()


async def add_course_lesson(
    session: AsyncSession,
    course_id: int,
    title: str,
    lesson_number: int,
    content: str | None = None,
):
    session.add(
        Lesson(
            course_id=course_id,
            title=title,
            lesson_number=lesson_number,
            content=content,
        )
    )
    await session.commit()


async def add_student_lesson(
    session: AsyncSession,
    student_id: int,
    lesson_id: int,
    date: datetime,
    homework: str | None = None,
):
    session.add(
        StudentLesson(
            student_id=student_id, lesson_id=lesson_id, homework=homework, date=date
        )
    )
    await session.commit()


async def add_user_schedule(
    session: AsyncSession,
    user_id: int,
    day_of_week: int,
    time: time,
    subject_id: int,
):
    user = await session.execute(select(User).where(User.id == user_id))
    if user.scalar_one_or_none():
        schedule = UserSchedule(
            user_id=user_id,
            day_of_week=day_of_week,
            start_time=time,
            course_id=subject_id,
        )
        session.add(schedule)
        await session.commit()


async def add_courses(
    session: AsyncSession, title: str, description: str, lesson_count: int
):
    course = Course(title=title, description=description, lesson_count=lesson_count)
    session.add(course)
    await session.commit()


async def get_user_by_telegram_id(
    session: AsyncSession, telegram_id: int, get_roles: bool = False
) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    if get_roles:
        stmt = stmt.options(selectinload(User.roles))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_role_by_name(session: AsyncSession, role_name: str) -> Role | None:
    result = await session.execute(select(Role).where(Role.name == role_name))
    return result.scalar_one_or_none()


async def get_admin(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession, all_profiles=False) -> list[User]:
    stmt = select(User)
    if all_profiles:
        stmt = stmt.options(
            selectinload(User.student_profile),
            selectinload(User.teacher_profile),
            selectinload(User.admin_profile),
        )

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_user_and_teacher_url_by_schedule(
    session: AsyncSession, schedule_id: int
) -> Tuple[int, str] | None:
    """
    Повертає (telegram_id, teacher_url) для користувача зі вказаним schedule_id.
    Якщо не знайдено — повертає None.
    """
    stmt = (
        select(User.telegram_id, User.telegram_name, Enrollment.teacher_url)
        .join(UserSchedule, User.id == UserSchedule.user_id)
        .join(Enrollment, UserSchedule.course_id == Enrollment.course_id)
        .join(Student, Enrollment.student_id == Student.id)
        .where(UserSchedule.id == schedule_id)
    )

    result = await session.execute(stmt)
    return result.one_or_none()


async def get_user_schedule(session: AsyncSession, user_id: int) -> list[UserSchedule]:
    stmt = (
        select(UserSchedule)
        .options(selectinload(UserSchedule.course))
        .where(UserSchedule.user_id == user_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_student_lessons(session: AsyncSession, student_id: int, period: int):
    now = datetime.now()
    stmt = (
        select(StudentLesson)
        .options(selectinload(StudentLesson.lesson))
        .where(StudentLesson.student_id == student_id)
        .where(StudentLesson.date > now - timedelta(days=period))
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_student_info(session: AsyncSession, student_id: int) -> Student | None:
    result = await session.execute(
        select(Student)
        .options(selectinload(Student.lessons))
        .where(Student.id == student_id)
    )
    return result.scalar_one_or_none()


from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


async def get_teacher_enrollments_with_student(session: AsyncSession, teacher_id: int):
    stmt = (
        select(Enrollment)
        .select_from(Enrollment)
        .where(Enrollment.teacher_id == teacher_id)
        .options(
            selectinload(Enrollment.student).selectinload(Student.user),
            selectinload(Enrollment.course),
        )
    )

    result = await session.execute(stmt)
    enrollments = result.scalars().all()
    return enrollments
