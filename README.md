# Wellness-Habit-Tracker (CLI)

A lightweight, terminal-based wellness habit tracker built with **Python3** and **SQLite**.  
This project helps users create, log, and track healthy habits such as exercise, hydration, sleep, and mindfulness.  
It runs fully **offline** in the Command Line Interface (CLI) — no internet or heavy GUI required.  

---
Video url =>(https://youtu.be/Fgb8ovHYI2Y)

## Features
- Add a wellness habits  
- View and manage all habits  
- Delete habits you no longer want to track 
- Log daily progress for each habit  
- View logs for accountability  
- Generate a simple progress reports  
 

---

## Requirements
- Python 3.x  
- SQLite (bundled with Python, no extra setup required)  

---
## Database schema

+-------------------+          +-------------------+          +-------------------+
|      users        |          |      habits       |          |       logs        |
+-------------------+          +-------------------+          +-------------------+
| id (PK)           |◄───┐     | id (PK)           |◄───┐     | id (PK)           |
| username          |    │     | name              |    │     | habit_id (FK)     |
| email             |    └────▶| description       |    └────▶| date              |
| created_at        |          | created_at        |          | progress          |
+-------------------+          | user_id (FK)      |          | notes             |
                               +-------------------+          +-------------------+

                               +-------------------+


habits: Stores habit details
logs: Stores daily progress for each habit

>A habit can have many logs (1-to-many relationship).

## Usage
To run our project, cd into **/CODECHALLENGES/Wellness-Habit-Tracker/Lib$** 
then run **python3 main.py**
===== Wellness Habit Tracker =====
1. Add Habit
2. View Habits
3. Delete Habit
4. Log Progress
5. View Logs
6. View Reports
0. Exit

choose 1 to add a habit
choose 2 to view habits
choose 3 to delete a habit
choose 4 to add log progress to habits
choose 5 to view habit logs
choose 5 to view the generated report and history of our habits
choose 0 to exit
