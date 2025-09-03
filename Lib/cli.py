from db import Base, engine, SessionLocal
from models import User, Habit, Log
import reports
from datetime import date

def setup_database():
    Base.metadata.create_all(engine)

def login_or_register(session):
    username = input("Enter your username: ").strip()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        user = User(username=username)
        session.add(user)
        session.commit()
        print(f"👤 New user created: {username}")
    else:
        print(f"👋 Welcome back, {username}")
    return user

def menu():
    print("\n=== Wellness Habit Tracker ===")
    print("1. Add a new habit")
    print("2. View habits")
    print("3. Delete a habit")
    print("4. Log progress")
    print("5. View habit logs")
    print("6. View reports")
    print("0. Exit")

def add_habit(session, user):
    name = input("Enter habit name: ")
    description = input("Enter description (optional): ")
    habit = Habit(user_id=user.id, name=name, description=description)
    session.add(habit)
    session.commit()
    print(f"✅ Habit '{habit.name}' added!")

def view_habits(session, user):
    habits = session.query(Habit).filter_by(user_id=user.id).all()
    if not habits:
        print("No habits found.")
    else:
        print("\nYour Habits:")
        for habit in habits:
            print(f"[{habit.id}] {habit.name} - {habit.description or 'No description'}")
    return habits

def delete_habit(session, user):
    habits = view_habits(session, user)
    if not habits:
        return
    habit_id = input("Enter the ID of the habit to delete: ")
    if habit_id.isdigit():
        habit = session.query(Habit).filter_by(id=int(habit_id), user_id=user.id).first()
        if habit:
            session.delete(habit)
            session.commit()
            print("🗑 Habit deleted.")
        else:
            print("Habit not found.")
    else:
        print("Invalid ID.")

def log_progress(session, user):
    habits = view_habits(session, user)
    if not habits:
        return
    habit_id = input("Enter the ID of the habit to log progress for: ")
    if not habit_id.isdigit():
        print("Invalid ID.")
        return
    status = input("Enter status (completed/missed/partial): ").strip().lower()
    notes = input("Optional notes: ")
    log = Log(habit_id=int(habit_id), status=status, notes=notes, log_date=date.today())
    session.add(log)
    session.commit()
    print(f"📌 Progress logged for habit ID {habit_id} on {log.log_date}")

def view_logs(session, user):
    habits = view_habits(session, user)
    if not habits:
        return
    habit_id = input("Enter the ID of the habit to view logs for: ")
    if not habit_id.isdigit():
        print("Invalid ID.")
        return
    logs = session.query(Log).filter_by(habit_id=int(habit_id)).order_by(Log.log_date.desc()).all()
    if not logs:
        print("No logs found for this habit.")
    else:
        print(f"\nLogs for Habit ID {habit_id}:")
        for log in logs:
            print(f"- {log.log_date}: {log.status} ({log.notes or 'No notes'})")

def view_reports(session, user):
    habits = session.query(Habit).filter_by(user_id=user.id).all()
    if not habits:
        print("No habits found.")
        return
    print("\n📊 Reports:")
    for habit in habits:
        rate = reports.completion_rate(session, habit.id)
        streak_val = reports.streak(session, habit.id)
        print(f"[{habit.id}] {habit.name} → {rate}% completed | Current streak: {streak_val} days")

    print("\n🏆 Top Habits:")
    for name, rate in reports.top_habits(session, user.id):
        print(f"- {name}: {rate}% completion")

def main():
    setup_database()
    session = SessionLocal()
    user = login_or_register(session)

    while True:
        menu()
        choice = input("Choose an option: ")
        if choice == "1": add_habit(session, user)
        elif choice == "2": view_habits(session, user)
        elif choice == "3": delete_habit(session, user)
        elif choice == "4": log_progress(session, user)
        elif choice == "5": view_logs(session, user)
        elif choice == "6": view_reports(session, user)
        elif choice == "0":
            print("See ya 👋")
            break
        else:
            print("Invalid choice, try again.")
    session.close()

if __name__ == "__main__":
    main()
