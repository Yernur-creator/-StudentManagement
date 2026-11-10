from database import get_connection, create_database
from student import add_student, delete_student, find_student


# 1. Студентке баға қосу
def add_grade(student_id, subject, grade):
    if not subject.strip():
        raise ValueError("Пән атауы бос болмауы керек!")

    if not 0 <= grade <= 100:
        raise ValueError("Баға 0 мен 100 аралығында болуы керек!")

    if find_student(student_id) is None:
        raise ValueError("Мұндай ID нөмірі бар студент табылмады!")

    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO grades (student_id, subject, grade)
            VALUES (?, ?, ?)
        """, (student_id, subject.strip(), grade))

        return cursor.lastrowid


# 2. Студенттің бағаларын көрсету
def get_student_grades(student_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT id, subject, grade
            FROM grades
            WHERE student_id = ?
            ORDER BY subject
        """, (student_id,))

        return cursor.fetchall()


# 3. Орташа балды есептеу
def calculate_average(student_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT AVG(grade)
            FROM grades
            WHERE student_id = ?
        """, (student_id,))

        result = cursor.fetchone()[0]

        if result is None:
            return None

        return round(result, 2)


# 4. Үлгерімі жоғары студенттерді анықтау
def get_top_students(min_average=85):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT
                s.id,
                s.full_name,
                s.student_group,
                ROUND(AVG(g.grade), 2) AS average_grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            GROUP BY s.id, s.full_name, s.student_group
            HAVING AVG(g.grade) >= ?
            ORDER BY average_grade DESC
        """, (min_average,))

        return cursor.fetchall()


# 5. Студенттерді орташа бал бойынша сұрыптау
def sort_students_by_average():
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT
                s.id,
                s.full_name,
                s.student_group,
                ROUND(AVG(g.grade), 2) AS average_grade
            FROM students s
            LEFT JOIN grades g ON s.id = g.student_id
            GROUP BY s.id, s.full_name, s.student_group
            ORDER BY
                average_grade IS NULL,
                average_grade DESC,
                s.full_name
        """)

        return cursor.fetchall()


# Бағдарламаны тексеру
if __name__ == "__main__":
    create_database()

    print("\n=== СТУДЕНТТЕРДІҢ БАҒАЛАРЫН БАСҚАРУ ===")

    # Тестілеу үшін студенттерді тіркеу
    student1 = add_student(
        "Рысбек Ернұр",
        "3ПО-624",
        17,
        "87089790141"
    )

    student2 = add_student(
        "Жакишева Сафина",
        "3ПО-624",
        18,
        "87079876543"
    )

    # Бірінші студенттің бағалары
    add_grade(student1, "Java-да бағдарламалау", 90)
    add_grade(student1, "Алгоритмдеу және бағдарламалау", 95)
    add_grade(student1, "Бағдарламалық қамтамасыз етуді әзірлеудің технологиясын жобалау", 85)

    # Екінші студенттің бағалары
    add_grade(student2, "Java-да бағдарламалау", 75)
    add_grade(student2, "Алгоритмдеу және бағдарламалау", 80)
    add_grade(student2, "Бағдарламалық қамтамасыз етуді әзірлеудің технологиясын жобалау", 70)

    print("\n1-студенттің бағалары:")
    for grade in get_student_grades(student1):
        print(grade)

    print("\n1-студенттің орташа балы:")
    print(calculate_average(student1))

    print("\n2-студенттің орташа балы:")
    print(calculate_average(student2))

    print("\nҮлгерімі жоғары студенттер:")
    for student in get_top_students():
        print(student)

    print("\nОрташа бал бойынша сұрыптау:")
    for student in sort_students_by_average():
        print(student)

    # Тестілеу деректерін жою
    delete_student(student1)
    delete_student(student2)

    print("\nТестілеу аяқталды!")