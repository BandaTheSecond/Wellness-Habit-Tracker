from sqlalchemy.orm import Session
from habits import Log, Habit

def completion_rate(session: Session, habit_id: int) -> float:
    logs = session.query(Log).filter_by(habit_id=habit_id).all()
    if not logs:
        return 0.0

    total_score = 0
    for log in logs:
        if log.status == "completed":
            total_score += 100
        elif log.status == "partial":
            total_score += 50
        elif log.status == "missed":
            total_score += 0

    return round(total_score / len(logs), 2)


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
