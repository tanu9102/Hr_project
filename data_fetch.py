import sqlite3
import pandas as pd
import streamlit as st
from utils import format_date, calculate_tenure, generate_sql_filter
from contextlib import closing

# Reuse DB connection via @st.cache_resource
@st.cache_resource
def get_db_connection():
    db_path = 'db/hr_analytics.db'
    conn = sqlite3.connect(db_path, check_same_thread=False)  # Allow multi-threading
    return conn

# Fetch data with safe parameterized queries
def fetch_data(query, params=None):
    # Use context manager to ensure connection is properly closed
    conn = get_db_connection()  # Use the cached connection

    try:
        with closing(conn.cursor()) as cursor: # 'with' ensures the cursor is automatically closed after execution
            data = pd.read_sql_query(query, conn, params=params)
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    return data

# Fetch performance trends with window functions for year-over-year performance
@st.cache_data  
def get_performance_trends(department_filter, date_range_filter, performance_threshold):
    query = '''
    WITH performance_ranks AS (
        SELECT e.name, p.review_date, p.score,
               ROW_NUMBER() OVER (PARTITION BY e.emp_id ORDER BY p.review_date) AS performance_rank
        FROM performance_reviews p
        JOIN employees e ON p.emp_id = e.emp_id
        JOIN departments d ON e.department_id = d.dept_id
        WHERE d.name = ? 
          AND p.review_date BETWEEN ? AND ? 
          AND p.score >= ? 
    )
    SELECT name, review_date, score, performance_rank
    FROM performance_ranks
    ORDER BY name, review_date;
    '''
    
    start_date, end_date = ('2010-01-01', '2025-12-31') if not date_range_filter else date_range_filter
    params = (department_filter, start_date, end_date, performance_threshold)
    return fetch_data(query, params=params)

# Fetch department performance (average performance score by department)
@st.cache_data  
def get_department_performance(department_filter):
    query = '''
    SELECT d.name as department, AVG(p.score) as avg_score
    FROM performance_reviews p
    JOIN employees e ON p.emp_id = e.emp_id
    JOIN departments d ON e.department_id = d.dept_id
    WHERE d.name = ?
    GROUP BY d.name;
    '''
    return fetch_data(query, params=(department_filter,))

# Fetch attrition rate (monthly exit counts)
@st.cache_data  
def get_attrition_rate(department_filter, start_date, end_date):
    query = '''
    SELECT strftime('%Y-%m', exit_date) as month, COUNT(*) as exits
    FROM employees
    WHERE exit_date IS NOT NULL
    AND department_id = (SELECT dept_id FROM departments WHERE name = ?)
    AND exit_date BETWEEN ? AND ?
    GROUP BY month;
    '''
    return fetch_data(query, params=(department_filter, start_date, end_date))

# Fetch department load (headcount & avg daily hours logged) with date range filter
@st.cache_data  
def get_department_load(department_filter, start_date, end_date):
    query = '''
    WITH active_employees AS (
        SELECT emp_id
        FROM employees e
        JOIN departments d ON e.department_id = d.dept_id
        WHERE d.name = ? 
          AND (e.exit_date IS NULL OR e.exit_date > DATE('now'))
    ),
    hours_per_day AS (
        SELECT e.department_id, ep.log_date, AVG(ep.hours_logged) as avg_hours_logged
        FROM employee_projects ep
        JOIN employees e ON ep.emp_id = e.emp_id
        JOIN departments d ON e.department_id = d.dept_id
        WHERE d.name = ? 
          AND ep.log_date BETWEEN ? AND ?
        GROUP BY e.department_id, ep.log_date
    )
    SELECT d.name as department,
           (SELECT COUNT(*) FROM active_employees) as current_headcount,
           h.log_date,
           ROUND(h.avg_hours_logged, 2) as avg_hours_logged_per_employee
    FROM departments d
    JOIN hours_per_day h ON d.dept_id = h.department_id
    WHERE d.name = ?
    ORDER BY h.log_date;
    '''
    params = (department_filter, department_filter, start_date, end_date, department_filter)
    return fetch_data(query, params=params)

# Fetch overlapping projects per employee
@st.cache_data  
def get_project_overlap(department_filter):
    query = '''
    SELECT e.name, p1.name as project1, p2.name as project2
    FROM employees e
    JOIN employee_projects ep1 ON e.emp_id = ep1.emp_id
    JOIN employee_projects ep2 ON ep1.emp_id = ep2.emp_id
    JOIN projects p1 ON ep1.project_id = p1.project_id
    JOIN projects p2 ON ep2.project_id = p2.project_id
    WHERE p1.start_date < p2.end_date AND p2.start_date < p1.end_date
      AND p1.project_id != p2.project_id
    AND e.department_id = (SELECT dept_id FROM departments WHERE name = ?)
    GROUP BY e.name, project1, project2;
    '''
    return fetch_data(query, params=(department_filter,))


# Updated query for employee tenure ladder
@st.cache_data  
def get_employee_tenure_ladder(department_filter):
    query = '''
    SELECT emp_id, name, join_date, exit_date,
           ROUND(
               (julianday(COALESCE(exit_date, CURRENT_DATE)) - julianday(join_date)) / 365.0, 2
           ) AS tenure_years
    FROM employees
    WHERE department_id = (SELECT dept_id FROM departments WHERE name = ?)
      AND join_date IS NOT NULL
      AND julianday(join_date) <= julianday(CURRENT_DATE);
    '''
    tenure_data = fetch_data(query, params=(department_filter,))
    
    # Ensure tenure is non-negative (in case of any edge cases with dates)
    if tenure_data is not None:
        tenure_data['tenure_years'] = tenure_data['tenure_years'].apply(lambda x: max(0, x))  # Ensuring no negative values
    return tenure_data


# Fetch employee project timelines for Gantt chart visualization
@st.cache_data  
def get_employee_project_timelines(department_filter):
    query = '''
    SELECT e.name AS employee_name, p.name AS project_name, ep.hours_logged, p.start_date, p.end_date
    FROM employees e
    JOIN employee_projects ep ON e.emp_id = ep.emp_id
    JOIN projects p ON ep.project_id = p.project_id
    WHERE e.department_id = (SELECT dept_id FROM departments WHERE name = ?)
    ORDER BY e.name, p.start_date;
    '''
    return fetch_data(query, params=(department_filter,))
