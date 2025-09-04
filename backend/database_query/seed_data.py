import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from faker import Faker
import random
import datetime

# DB connection params
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "root"
DB_NAME = "education_platform"

fake = Faker()

# Step 1: Connect to Postgres (default 'postgres' DB) and create new DB
def create_database():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
    cur.execute(f"CREATE DATABASE {DB_NAME};")
    cur.close()
    conn.close()
    print(f"Database {DB_NAME} created successfully!")

# Step 2: Create schema (tables)
def create_tables():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        role VARCHAR(20), -- student, instructor
        created_at TIMESTAMP
    );
    """)
    cur.execute("""
    CREATE TABLE courses (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200),
        description TEXT,
        price NUMERIC(10,2),
        instructor_id INT REFERENCES users(id),
        created_at TIMESTAMP
    );
    """)
    cur.execute("""
    CREATE TABLE enrollments (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        course_id INT REFERENCES courses(id),
        enrolled_at TIMESTAMP
    );
    """)
    cur.execute("""
    CREATE TABLE payments (
        id SERIAL PRIMARY KEY,
        enrollment_id INT REFERENCES enrollments(id),
        amount NUMERIC(10,2),
        paid_at TIMESTAMP,
        status VARCHAR(20)
    );
    """)
    cur.execute("""
    CREATE TABLE lessons (
        id SERIAL PRIMARY KEY,
        course_id INT REFERENCES courses(id),
        title VARCHAR(200),
        content TEXT,
        duration INT, -- in minutes
        created_at TIMESTAMP
    );
    """)
    cur.execute("""
    CREATE TABLE reviews (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        course_id INT REFERENCES courses(id),
        rating INT,
        comment TEXT,
        created_at TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully!")

# Step 3: Populate tables with random data
def populate_data():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )
    cur = conn.cursor()

    # Users (students + instructors)
    for _ in range(600):
        cur.execute(
            "INSERT INTO users (name, email, role, created_at) VALUES (%s, %s, %s, %s)",
            (
                fake.name(),
                fake.unique.email(),
                random.choice(["student", "instructor"]),
                fake.date_time_this_decade(),
            ),
        )

    # Courses
    cur.execute("SELECT id FROM users WHERE role='instructor'")
    instructor_ids = [row[0] for row in cur.fetchall()]
    for _ in range(500):
        cur.execute(
            "INSERT INTO courses (title, description, price, instructor_id, created_at) VALUES (%s, %s, %s, %s, %s)",
            (
                fake.sentence(nb_words=5),
                fake.paragraph(nb_sentences=3),
                round(random.uniform(20, 200), 2),
                random.choice(instructor_ids),
                fake.date_time_this_decade(),
            ),
        )

    # Enrollments
    cur.execute("SELECT id FROM users WHERE role='student'")
    student_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM courses")
    course_ids = [row[0] for row in cur.fetchall()]
    for _ in range(1000):
        cur.execute(
            "INSERT INTO enrollments (user_id, course_id, enrolled_at) VALUES (%s, %s, %s)",
            (
                random.choice(student_ids),
                random.choice(course_ids),
                fake.date_time_this_year(),
            ),
        )

    # Payments
    cur.execute("SELECT id FROM enrollments")
    enrollment_ids = [row[0] for row in cur.fetchall()]
    for eid in enrollment_ids:
        cur.execute(
            "INSERT INTO payments (enrollment_id, amount, paid_at, status) VALUES (%s, %s, %s, %s)",
            (
                eid,
                round(random.uniform(20, 200), 2),
                fake.date_time_this_year(),
                random.choice(["paid", "failed", "pending"]),
            ),
        )

    # Lessons
    for cid in course_ids:
        for _ in range(random.randint(5, 15)):
            cur.execute(
                "INSERT INTO lessons (course_id, title, content, duration, created_at) VALUES (%s, %s, %s, %s, %s)",
                (
                    cid,
                    fake.sentence(nb_words=6),
                    fake.text(max_nb_chars=500),
                    random.randint(5, 60),
                    fake.date_time_this_year(),
                ),
            )

    # Reviews
    for _ in range(800):
        cur.execute(
            "INSERT INTO reviews (user_id, course_id, rating, comment, created_at) VALUES (%s, %s, %s, %s, %s)",
            (
                random.choice(student_ids),
                random.choice(course_ids),
                random.randint(1, 5),
                fake.sentence(),
                fake.date_time_this_year(),
            ),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Data populated successfully!")

if __name__ == "__main__":
    create_database()
    create_tables()
    populate_data()
