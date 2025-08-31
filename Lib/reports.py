from db import get_connection

def completion_rate(habit_id):
    """Calculate % of completed logs for a habit"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs WHERE habit_id = ?", (habit_id,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE habit_id = ? AND status = 'completed'", (habit_id,))
    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0
    return round((completed / total) * 100, 2)

def streak(habit_id):
    """Calculate current streak of consecutive 'completed' days"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT log_date, status FROM logs WHERE habit_id = ? ORDER BY log_date DESC",
        (habit_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    streak_count = 0
    for row in rows:
        status = row[1]
        if status == "completed":
            streak_count += 1
        else:
            break  # streak ends when first non-completed is found

    return streak_count
