import sqlite3
from db import get_connection

class Habit:
    def __init__(self, name, description=None, id=None):
        self.id = id
        self.name = name
        self.description = description

    def save(self):
        """Insert habit into database"""
        conn = get_connection()
        cursor = conn.cursor()

        if self.id:  # update existing habit
            cursor.execute(
                "UPDATE habits SET name = ?, description = ? WHERE id = ?",
                (self.name, self.description, self.id)
            )
        else:  # insert new habit
            cursor.execute(
                "INSERT INTO habits (name, description) VALUES (?, ?)",
                (self.name, self.description)
            )
            self.id = cursor.lastrowid

        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        """Return list of all habits"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, description FROM habits")
        rows = cursor.fetchall()
        conn.close()

        return [Habit(id=row[0], name=row[1], description=row[2]) for row in rows]

    @staticmethod
    def delete(habit_id):
        """Delete a habit by id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
        conn.close()
