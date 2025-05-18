import sqlite3
from random import randint, choice
from datetime import datetime, timedelta

# Function to generate random dates
def generate_random_date(start_year=2010, end_year=2021):
    start_date = datetime(randint(start_year, end_year), randint(1, 12), randint(1, 28))
    return start_date.strftime('%Y-%m-%d')

# Function to generate random employee data
def generate_employee_data(num_employees=100):
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Helen', 'Ivy', 'Jack', 
             'Karen', 'Liam', 'Mason', 'Nina', 'Oscar', 'Paul', 'Quincy', 'Rachel', 'Sam', 'Tom', 
             'Uma', 'Vera', 'Will', 'Xander', 'Yara', 'Zane']
    departments = [1, 2, 3, 4, 5]  # Department IDs 1 to 5
    genders = ['M', 'F']
    
    employees = []
    for i in range(num_employees):
        name = choice(names)
        age = randint(22, 55)
        gender = choice(genders)
        department_id = choice(departments)
        join_date = generate_random_date()
        exit_date = None if randint(0, 1) else generate_random_date()  # Some employees may still be working
        employees.append((name, age, gender, department_id, join_date, exit_date))
    
    return employees

# Function to generate random performance reviews
def generate_performance_reviews(num_reviews=100):
    reviews = []
    for i in range(num_reviews):
        emp_id = randint(1, 100)  # Random employee ID
        review_date = generate_random_date(2019, 2022)
        score = randint(1, 10)
        reviewer_id = randint(1, 5)  # Random reviewer ID
        reviews.append((emp_id, review_date, score, reviewer_id))
    
    return reviews

# Function to generate random projects
def generate_projects(num_projects=10):
    projects = []
    for i in range(num_projects):
        project_name = f'Project {chr(65+i)}'
        start_date = generate_random_date(2020, 2022)
        end_date = generate_random_date(2022, 2023)
        projects.append((project_name, start_date, end_date))
    
    return projects

# Function to generate daily employee-project assignments
def generate_employee_projects(num_assignments=200):
    assignments = []
    for i in range(num_assignments):
        emp_id = randint(1, 100)
        project_id = randint(1, 10)
        hours_logged = randint(1, 8)  # Simulate daily log (1 to 8 hours)
        log_date = generate_random_date(2011, 2024)  # Log dates in recent years
        assignments.append((emp_id, project_id, hours_logged, log_date))
    return assignments

# Create a connection to SQLite database
conn = sqlite3.connect('hr_analytics.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    department_id INTEGER,
    join_date TEXT,
    exit_date TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    dept_id INTEGER PRIMARY KEY,
    name TEXT,
    head_id INTEGER
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS performance_reviews (
    emp_id INTEGER,
    review_date TEXT,
    score INTEGER,
    reviewer_id INTEGER,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    name TEXT,
    start_date TEXT,
    end_date TEXT
);
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS employee_projects (
    emp_id INTEGER,
    project_id INTEGER,
    hours_logged INTEGER,
    log_date TEXT,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
''')

# Clear existing data
cursor.executescript('''
DELETE FROM employee_projects;
DELETE FROM projects;
DELETE FROM performance_reviews;
DELETE FROM employees;
DELETE FROM departments;
''')

# Insert departments (at least 5 departments)
cursor.executemany('''
INSERT INTO departments (name, head_id) VALUES (?, ?)
''', [
    ('HR', 1),
    ('Engineering', 2),
    ('Sales', 3),
    ('Marketing', 4),
    ('Finance', 5)
])

# Insert employees (100 employees)
employee_data = generate_employee_data(100)
cursor.executemany('''
INSERT INTO employees (name, age, gender, department_id, join_date, exit_date) VALUES (?, ?, ?, ?, ?, ?)
''', employee_data)

# Insert performance reviews (100 reviews)
performance_reviews = generate_performance_reviews(100)
cursor.executemany('''
INSERT INTO performance_reviews (emp_id, review_date, score, reviewer_id) VALUES (?, ?, ?, ?)
''', performance_reviews)

# Insert projects (10 projects)
projects = generate_projects(10)
cursor.executemany('''
INSERT INTO projects (name, start_date, end_date) VALUES (?, ?, ?)
''', projects)

# Insert employee projects with log_date
employee_projects = generate_employee_projects(200)
cursor.executemany('''
INSERT INTO employee_projects (emp_id, project_id, hours_logged, log_date) VALUES (?, ?, ?, ?)
''', employee_projects)

# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ Database setup complete with daily logging enabled in employee_projects.")
