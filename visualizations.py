import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


# Helper function to check if data is valid (not None and not empty)
def validate_data(data, data_name):
    if data is None or data.empty:
        st.warning(f"No {data_name} data available.")
        return False
    return True

# Helper function to handle exception and return None
def plot_with_error_handling(plot_func, *args, **kwargs):
    try:
        return plot_func(*args, **kwargs)
    except Exception as e:
        st.error(f"Error: {e}")
        return None


# Plot employee performance trends over time
def plot_performance_trends(performance_data):
    if validate_data(performance_data, "performance"):
        performance_data['review_date'] = pd.to_datetime(performance_data['review_date'], errors='coerce')
        performance_data.dropna(subset=['review_date'], inplace=True)

        if performance_data.empty:
            st.warning("All review dates were invalid. No data to plot.")
            return None

        return plot_with_error_handling(
            px.line,
            performance_data,
            x="review_date",
            y="score",
            color="name",
            markers=True,
            title="Employee Performance Trends"
        )

# Plot average performance score by department using boxplot
def plot_department_performance(department_performance):
    if validate_data(department_performance, "department performance"):
        return plot_with_error_handling(
            px.box,
            department_performance,
            x="department",
            y="avg_score",
            title="Performance Score Distribution by Department"
        )

# Plot monthly attrition rate using line chart
def plot_attrition_rate(attrition_data):
    if validate_data(attrition_data, "attrition"):
        return plot_with_error_handling(
            px.line,
            attrition_data,
            x="month",
            y="exits",
            markers=True,
            title="Monthly Attrition Rate"
        )

# Plot department load over time using dual-axis line chart
def plot_department_load(department_load):
    if validate_data(department_load, "department load") and {'log_date', 'current_headcount', 'avg_hours_logged_per_employee'}.issubset(department_load.columns):
        department_load['log_date'] = pd.to_datetime(department_load['log_date'], errors='coerce')
        department_load.dropna(subset=['log_date', 'current_headcount', 'avg_hours_logged_per_employee'], inplace=True)

        return plot_with_error_handling(
            make_subplots,
            specs=[[{"secondary_y": True}]],
            trace_1={
                "x": department_load['log_date'],
                "y": department_load['current_headcount'],
                "name": 'Headcount',
                "mode": 'lines+markers',
                "line": dict(color='indianred')
            },
            trace_2={
                "x": department_load['log_date'],
                "y": department_load['avg_hours_logged_per_employee'],
                "name": 'Avg Hours Logged',
                "mode": 'lines+markers',
                "line": dict(color='steelblue')
            },
            title=f"{department_load['department'].iloc[0]} Department Load Over Time"
        )

    
# Plot employee tenure ladder using scatter plot
def plot_employee_tenure_ladder(tenure_ladder):
    if validate_data(tenure_ladder, "tenure ladder"):
        tenure_ladder = tenure_ladder.sort_values(by='tenure_years', ascending=False)

        return plot_with_error_handling(
            px.scatter,
            tenure_ladder,
            x="tenure_years",
            y="name",
            size_max=10,
            title="Employee Tenure Ladder",
            labels={"tenure_years": "Tenure (Years)", "name": "Employee Name"}
        )


# Plot Employee Project Timelines (Gantt chart)
def plot_employee_project_timelines(project_timelines_data):
    if validate_data(project_timelines_data, "project timelines"):
        return plot_with_error_handling(
            px.timeline,
            project_timelines_data,
            x_start="start_date",
            x_end="end_date",
            y="employee_name",
            color="project_name",
            title="Employee Project Timelines"
        )
