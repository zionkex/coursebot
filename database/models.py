from datetime import datetime, timezone, time
from typing import Optional
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    BigInteger,
    DateTime,
    ForeignKey,
    Time,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base

Base = declarative_base()

user_roles_association = Table(
    "user_roles_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(
        secondary=user_roles_association,
        back_populates="roles",
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    telegram_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    telegram_username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    roles: Mapped[list[Role]] = relationship(
        secondary=user_roles_association,
        back_populates="users",
        cascade="all",
    )
    student_profile: Mapped[Optional["Student"]] = relationship(
        "Student", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    teacher_profile: Mapped[Optional["Teacher"]] = relationship(
        "Teacher", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    admin_profile: Mapped[Optional["Admin"]] = relationship(
        "Admin", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    schedules: Mapped[list["UserSchedule"]] = relationship(
        "UserSchedule", back_populates="user", cascade="all, delete-orphan"
    )


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    user: Mapped["User"] = relationship(
        "User", back_populates="student_profile", uselist=False
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        "Enrollment", back_populates="student", cascade="all, delete-orphan"
    )
    lessons: Mapped[list["StudentLesson"]] = relationship(
        "StudentLesson", back_populates="student", cascade="all, delete-orphan"
    )


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user: Mapped["User"] = relationship(
        "User", back_populates="teacher_profile", uselist=False
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        "Enrollment", back_populates="teacher", cascade="all, delete-orphan"
    )


class Admin(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user: Mapped["User"] = relationship(
        "User", back_populates="admin_profile", uselist=False
    )


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lesson_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    enrollments: Mapped[list["Enrollment"]] = relationship(
        "Enrollment", back_populates="course", cascade="all, delete-orphan"
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="course", cascade="all, delete-orphan"
    )

    course_schedules: Mapped["UserSchedule"] = relationship(
        "UserSchedule", back_populates="course"
    )


class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False
    )
    teacher_url: Mapped[str] = mapped_column(String(255), nullable=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    student: Mapped["Student"] = relationship("Student", back_populates="enrollments")
    course: Mapped["Course"] = relationship("Course", back_populates="enrollments")
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="enrollments")


class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    lesson_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    course: Mapped["Course"] = relationship("Course", back_populates="lessons")
    student_lessons: Mapped[list["StudentLesson"]] = relationship(
        "StudentLesson", back_populates="lesson", cascade="all, delete-orphan"
    )


class StudentLesson(Base):
    __tablename__ = "student_lessons"
    id = mapped_column(Integer, primary_key=True)
    student_id = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    lesson_id = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )

    homework = mapped_column(String, nullable=True)
    date = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    student = relationship("Student", back_populates="lessons")
    lesson = relationship("Lesson", back_populates="student_lessons")


class UserSchedule(Base):
    __tablename__ = "user_schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="SET NULL"), nullable=True
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="schedules")
    course: Mapped[Course] = relationship("Course", back_populates="course_schedules")
