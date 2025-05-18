import pandas as pd
from datetime import datetime
import io
import streamlit as st

# === DATE UTILITIES ===

def format_date(date_str: str) -> str:
    """Format a date string to 'Month DD, YYYY' format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    except ValueError:
        return "Invalid Date"

def format_date_range(start_date: str, end_date: str) -> str | None:
    """Return SQL-style BETWEEN clause for dates."""
    if start_date and end_date:
        return f"BETWEEN '{start_date}' AND '{end_date}'"
    return None

# === TENURE & ATTRITION ===

def calculate_tenure(join_date: str, exit_date: str | None = None) -> int | None:
    """Calculate tenure in months."""
    try:
        join = datetime.strptime(join_date, "%Y-%m-%d")
        exit = datetime.strptime(exit_date, "%Y-%m-%d") if exit_date else datetime.now()
        return (exit - join).days // 30
    except (ValueError, TypeError):
        return None

def calculate_monthly_attrition_rate(exits: int, total_employees: int) -> float:
    """Calculate monthly attrition as a percentage."""
    if total_employees == 0:
        return 0
    return (exits / total_employees) * 100

# === SQL HELPER FUNCTIONS ===

def generate_sql_filter(department: str = None, date_range: str = None, performance_threshold: int = None) -> str:
    """Build SQL WHERE clause from filters."""
    filters = []
    if department:
        filters.append(f"d.name = '{department}'")
    if date_range:
        filters.append(f"p.review_date {date_range}")
    if performance_threshold is not None:
        filters.append(f"p.score >= {performance_threshold}")
    return "WHERE " + " AND ".join(filters) if filters else ""

def generate_performance_trends_query(department: str = None, date_range: str = None, performance_threshold: int = None) -> str:
    """Return full SQL query for performance trends with optional filters."""
    base_query = '''
    SELECT e.name, p.review_date, p.score
    FROM performance_reviews p
    JOIN employees e ON p.emp_id = e.emp_id
    JOIN departments d ON e.department_id = d.dept_id
    '''
    filter_clause = generate_sql_filter(department, date_range, performance_threshold)
    if filter_clause:
        base_query += " " + filter_clause
    base_query += " ORDER BY e.name, p.review_date;"
    return base_query

# === MISC UTILITIES ===

def format_number(number) -> str:
    """Return formatted number with commas."""
    try:
        return f"{int(number):,}"
    except (ValueError, TypeError):
        return "N/A"

# === STREAMLIT DOWNLOAD UTILITIES ===

def download_plot(fig, filename: str):
    """Render download button for Plotly figure as PNG using in-memory buffer."""
    img_bytes = fig.to_image(format="png")
    buffer = io.BytesIO(img_bytes)
    st.download_button("Download Chart", data=buffer, file_name=filename, mime="image/png")

def download_as_excel(df: pd.DataFrame, filename: str):
    """Render download button for DataFrame as Excel."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    st.download_button("Download Excel", data=output, file_name=filename, mime="application/vnd.ms-excel")

def render_plot_with_download(fig, title: str, filename: str):
    """Display Plotly chart with title and download button."""
    if fig:
        st.subheader(title)
        st.plotly_chart(fig, use_container_width=True)
        download_plot(fig, filename)
