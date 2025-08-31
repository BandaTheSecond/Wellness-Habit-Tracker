from db import get_connection
from datetime import date

class Log:
    def __init__(self, habit_id, status, notes=None, log_date=None, id=None):
        self.id = id
        self.habit_id = habit_id
        self.status = status        # e.g. "completed", "missed", "partial"
        self.notes = notes
        self.log_date = log_date or date.today().isoformat()

    def save(self):
        """Insert a new log entry"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO logs (habit_id, log_date, status, notes) VALUES (?, ?, ?, ?)",
            (self.habit_id, self.log_date, self.status, self.notes)
        )
        self.id = cursor.lastrowid

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_habit(habit_id):
        """Fetch logs for a specific habit"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, habit_id, log_date, status, notes FROM logs WHERE habit_id = ? ORDER BY log_date DESC",
            (habit_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [Log(id=row[0], habit_id=row[1], log_date=row[2], status=row[3], notes=row[4]) for row in rows]
