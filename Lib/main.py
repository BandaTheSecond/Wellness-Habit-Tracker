from db import setup_database
from Habit import Habit

def menu():
    print("\n=== Wellness Habit Tracker ===")
    print("1. Add a new habit")
    print("2. View habits")
    print("3. Delete a habit")
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

def delete_habit():
    view_habits()
    habit_id = input("Enter the ID of the habit to delete: ")
    if habit_id.isdigit():
        Habit.delete(int(habit_id))
        print("🗑 Habit deleted.")
    else:
        print("Invalid ID.")

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
        elif choice == "0":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
