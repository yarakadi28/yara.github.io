import sqlite3

# Connect to SQLite (in memory for testing)
conn = sqlite3.connect(':memory:')

# this is important because foreign keys are OFF by default in SQLite
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# Helper function to inspect table contents
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))

# Create tables
cursor.execute("""
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")
cursor.execute("""
CREATE TABLE courses (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id))
""")
cursor.execute("""
CREATE TABLE grades (
    student_id INT,
    course_id INT,
    grade REAL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY(student_id) REFERENCES student(student_id)
)
""")
students = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21)
]
courses=[
    (1,101),(2,202),(3,103)
]
grades=[(1,101,70),(2,202,95),(3,103,50)]
cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades)
cursor.executemany("INSERT INTO courses VALUES (?, ?)", courses)
conn.commit()

print_table(cursor, "student")
cursor.execute("""
SELECT student_id,course_id, MAX(grade)
FROM grades 
WHERE student_id=1
               """)
print (cursor.fetchone())
cursor.execute("""
SELECT AVG(grade)
FROM grades
WHERE student_id=1
""")
print(cursor.fetchone())
# Example SELECT query
cursor.execute("SELECT * FROM student")
print("\nResult of: SELECT * FROM student")
for row in cursor.fetchall():
    print(row)

conn.close()