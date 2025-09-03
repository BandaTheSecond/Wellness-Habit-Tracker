from sqlalchemy.orm import Session
from models import Log, Habit

def completion_rate(session: Session, habit_id: int) -> float:
    total = session.query(Log).filter_by(habit_id=habit_id).count()
    completed = session.query(Log).filter_by(habit_id=habit_id, status="completed").count()
    return round((completed / total) * 100, 2) if total > 0 else 0.0

def streak(session: Session, habit_id: int) -> int:
    logs = (
        session.query(Log)
        .filter_by(habit_id=habit_id)
        .order_by(Log.log_date.desc())
        .all()
    )
    streak_count = 0
    for log in logs:
        if log.status == "completed":
            streak_count += 1
        else:
            break
    return streak_count

def top_habits(session: Session, user_id: int, limit: int = 3):
    habits = session.query(Habit).filter_by(user_id=user_id).all()
    stats = [(habit.name, completion_rate(session, habit.id)) for habit in habits]
    return sorted(stats, key=lambda x: x[1], reverse=True)[:limit]
