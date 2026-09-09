import sqlite3
from pathlib import Path


DATABASE_FOLDER = Path("database")
DATABASE_FOLDER.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_FOLDER / "company.db"


connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    salary INTEGER
)
""")


employees = [
    (1, "Rahul", "AI", "AI Intern", 25000),
    (2, "Amit", "IT", "Software Engineer", 55000),
    (3, "Priya", "HR", "HR Manager", 65000),
    (4, "Sneha", "Data Science", "Data Scientist", 75000),
    (5, "Rohan", "IT", "Backend Developer", 60000),
    (6, "Neha", "Finance", "Financial Analyst", 58000),
]


cursor.executemany("""
INSERT OR REPLACE INTO employees
(id, name, department, position, salary)
VALUES (?, ?, ?, ?, ?)
""", employees)


connection.commit()
connection.close()

print("Database created successfully.")
print(f"Location: {DATABASE_PATH}")
