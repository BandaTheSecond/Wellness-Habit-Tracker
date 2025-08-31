from db import setup_database
from Habit import Habit
from log import Log

def menu():
    print("\n=== Wellness Habit Tracker ===")
    print("1. Add a new habit")
    print("2. View habits")
    print("3. Delete a habit")
    print("4. Log progress")
    print("5. View habit logs")
    print("0. Exit")

def add_habit():
    name = input("Enter habit name: ")
    description = input("Enter description (optional): ")
    habit = Habit(name=name, description=description)
    habit.save()
    print(f"✅ Habit '{habit.name}' added!")

def view_habits():
    habits = Habit.get_all()
    if not habits:
        print("No habits found.")
    else:
        print("\nYour Habits:")
        for habit in habits:
            print(f"[{habit.id}] {habit.name} - {habit.description or 'No description'}")
    return habits

def delete_habit():
    habits = view_habits()
    if not habits:
        return
    habit_id = input("Enter the ID of the habit to delete: ")
    if habit_id.isdigit():
        Habit.delete(int(habit_id))
        print("🗑 Habit deleted.")
    else:
        print("Invalid ID.")

def log_progress():
    habits = view_habits()
    if not habits:
        return
    habit_id = input("Enter the ID of the habit to log progress for: ")
    if not habit_id.isdigit():
        print("Invalid ID.")
        return
    status = input("Enter status (completed/missed/partial): ").strip().lower()
    notes = input("Optional notes: ")
    log = Log(habit_id=int(habit_id), status=status, notes=notes)
    log.save()
    print(f"📌 Progress logged for habit ID {habit_id} on {log.log_date}")

def view_logs():
    habits = view_habits()
    if not habits:
        return
    habit_id = input("Enter the ID of the habit to view logs for: ")
    if not habit_id.isdigit():
        print("Invalid ID.")
        return
    logs = Log.get_by_habit(int(habit_id))
    if not logs:
        print("No logs found for this habit.")
    else:
        print(f"\nLogs for Habit ID {habit_id}:")
        for log in logs:
            print(f"- {log.log_date}: {log.status} ({log.notes or 'No notes'})")

def main():
    setup_database()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_habit()
        elif choice == "2":
            view_habits()
        elif choice == "3":
            delete_habit()
        elif choice == "4":
            log_progress()
        elif choice == "5":
            view_logs()
        elif choice == "0":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
