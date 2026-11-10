import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "students.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            student_group TEXT NOT NULL,
            age INTEGER,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            grade REAL NOT NULL CHECK (grade >= 0 AND grade <= 100),
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()

    print("Дерекқор сәтті құрылды!")


if __name__ == "__main__":
    create_database()