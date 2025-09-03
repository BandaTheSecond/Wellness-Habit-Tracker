from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import date
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="habits")
    logs = relationship("Log", back_populates="habit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Habit(id={self.id}, name={self.name}, user_id={self.user_id})>"


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    log_date = Column(Date, default=date.today)
    status = Column(String, nullable=False)  # ("completed", "missed", "partial")
    notes = Column(Text)

    habit = relationship("Habit", back_populates="logs")

    def __repr__(self):
        return f"<Log(id={self.id}, habit_id={self.habit_id}, date={self.log_date}, status={self.status})>"
