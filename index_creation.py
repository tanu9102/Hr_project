import sqlite3
import time

def create_indexes():
    # Connect to the database
    conn = sqlite3.connect('hr_analytics.db')
    cursor = conn.cursor()

    # Measure query performance before indexing (Before)
    start_time = time.time()
    cursor.execute('SELECT * FROM performance_reviews WHERE emp_id = 1')
    cursor.fetchall()  
    print("Time without index: {:.6f} seconds".format(time.time() - start_time))

    # Create indexes (if not already created)
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_reviews_emp_id ON performance_reviews(emp_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_reviews_review_date ON performance_reviews(review_date);')  
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_department_id ON employees(department_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_join_date ON employees(join_date);')  
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_exit_date ON employees(exit_date);')  
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employee_projects_project_id ON employee_projects(project_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employee_projects_log_date ON employee_projects(log_date);')  

    # Commit the changes
    conn.commit()

    # Measure query performance after indexing (After)
    start_time = time.time()
    cursor.execute('SELECT * FROM performance_reviews WHERE emp_id = 1')
    cursor.fetchall()  
    print("Time with index: {:.6f} seconds".format(time.time() - start_time))

    # Close the connection
    conn.close()

if __name__ == "__main__":
    create_indexes()
