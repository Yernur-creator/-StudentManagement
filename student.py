from database import get_connection, create_database


# 1. Студентті тіркеу
def add_student(full_name, student_group, age, phone):
    if not full_name.strip() or not student_group.strip():
        raise ValueError("Аты-жөні мен тобы міндетті түрде толтырылуы керек!")

    if age is not None and not (1 <= age <= 120):
        raise ValueError("Жас 1 мен 120 аралығында болуы керек!")

    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO students (full_name, student_group, age, phone)
            VALUES (?, ?, ?, ?)
        """, (full_name.strip(), student_group.strip(), age, phone))

        student_id = cursor.lastrowid

    return student_id


# 2. Барлық студенттерді көрсету
def get_all_students():
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT id, full_name, student_group, age, phone
            FROM students
            ORDER BY id
        """)

        return cursor.fetchall()


# 3. Студентті ID арқылы іздеу
def find_student(student_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT id, full_name, student_group, age, phone
            FROM students
            WHERE id = ?
        """, (student_id,))

        return cursor.fetchone()


# 4. Студент мәліметтерін өзгерту
def update_student(student_id, full_name, student_group, age, phone):
    if not full_name.strip() or not student_group.strip():
        raise ValueError("Аты-жөні мен тобы бос болмауы керек!")

    if age is not None and not (1 <= age <= 120):
        raise ValueError("Жас дұрыс енгізілмеген!")

    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE students
            SET full_name = ?,
                student_group = ?,
                age = ?,
                phone = ?
            WHERE id = ?
        """, (
            full_name.strip(),
            student_group.strip(),
            age,
            phone,
            student_id
        ))

        return cursor.rowcount > 0


# 5. Студентті жою
def delete_student(student_id):
    with get_connection() as connection:
        cursor = connection.execute("""
            DELETE FROM students
            WHERE id = ?
        """, (student_id,))

        return cursor.rowcount > 0


# Бағдарламаны тексеру
if __name__ == "__main__":
    create_database()

    print("\n=== СТУДЕНТТЕРДІ БАСҚАРУ ЖҮЙЕСІ ===")

    # Жаңа студентті тіркеу
    student_id = add_student(
        "Рысбек Ернұр",
        "3ПО-624",
        17,
        "87089790141"
    )

    print(f"\nСтудент тіркелді! ID: {student_id}")

    # Студенттер тізімі
    print("\nБарлық студенттер:")
    for student in get_all_students():
        print(student)

    # ID арқылы іздеу
    print("\nСтудентті іздеу:")
    print(find_student(student_id))

    # Мәліметтерді өзгерту
    update_student(
        student_id,
        "Рысбек Ернұр",
        "3ПО-624",
        17,
        "87089790141"
    )

    print("\nӨзгертілген мәлімет:")
    print(find_student(student_id))

    # Студентті жою
    delete_student(student_id)

    print("\nСтудент жойылды!")

    print("\nҚалған студенттер:")
    for student in get_all_students():
        print(student)