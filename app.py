import streamlit as st
import plotly.io as pio

from data_fetch import (
    get_performance_trends,
    get_department_performance,
    get_attrition_rate,
    get_department_load,
    get_project_overlap,
    get_employee_tenure_ladder,
    get_employee_project_timelines
)

from visualizations import (
    plot_performance_trends,
    plot_department_performance,
    plot_attrition_rate,
    plot_department_load,
    plot_employee_tenure_ladder,
    plot_employee_project_timelines
)

from utils import (
    download_plot,
    download_as_excel,
    render_plot_with_download
)

# Plotly rendering defaults
pio.kaleido.scope.default_scale = 1
pio.kaleido.scope.default_width = 700
pio.kaleido.scope.default_height = 450

# Constants
DEPARTMENTS = ['HR', 'Engineering', 'Sales', 'Marketing', 'Finance']
TAB_CONFIG = {
    "📈 Performance Trends": {"dates": True, "threshold": True, "fetch": "performance"},
    "🏢 Department Performance": {"dates": False, "threshold": False, "fetch": "department_perf"},
    "📉 Attrition Analysis": {"dates": True, "threshold": False, "fetch": "attrition"},
    "👥 Department Load": {"dates": True, "threshold": False, "fetch": "load"},
    "🧭 Tenure Ladder": {"dates": False, "threshold": False, "fetch": "tenure"},
    "🧩 Project Overlap": {"dates": False, "threshold": False, "fetch": "overlap"},
    "📅 Employee Project Timelines": {"dates": False, "threshold": False, "fetch": "timelines"},
}

# Streamlit Config
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")
st.title('📊 HR Analytics Dashboard')

# Sidebar Filters
selected_tab = st.selectbox("Select a Tab", list(TAB_CONFIG.keys()))
config = TAB_CONFIG[selected_tab]

department = st.sidebar.selectbox("Select Department", DEPARTMENTS)

start_date, end_date, threshold = None, None, None
if config["dates"]:
    st.sidebar.subheader("Select Date Range")
    start_year = st.sidebar.selectbox("Start Year", range(2015, 2026), index=0)
    end_year = st.sidebar.selectbox("End Year", range(2015, 2026), index=10)
    start_month = st.sidebar.selectbox("Start Month", range(1, 13), format_func=lambda x: f"{x:02d}")
    end_month = st.sidebar.selectbox("End Month", range(1, 13), format_func=lambda x: f"{x:02d}")
    start_date = f"{start_year}-{start_month:02d}-01"
    end_date = f"{end_year}-{end_month:02d}-28"

if config["threshold"]:
    threshold = st.sidebar.slider("Performance Score Threshold", 0, 10, 5)

# --- Cached Fetch Functions ---
@st.cache_data
def fetch_performance(dept, date_range, thresh):
    return get_performance_trends(dept, date_range, thresh)

@st.cache_data
def fetch_department_performance(dept):
    return get_department_performance(dept)

@st.cache_data
def fetch_attrition(dept, start, end):
    return get_attrition_rate(dept, start, end)

@st.cache_data
def fetch_department_load(dept, start, end):
    return get_department_load(dept, start, end)

@st.cache_data
def fetch_tenure(dept):
    return get_employee_tenure_ladder(dept)

@st.cache_data
def fetch_overlap(dept):
    return get_project_overlap(dept)

@st.cache_data
def fetch_timelines(dept):
    return get_employee_project_timelines(dept)

# --- Tab Logic ---
if config["fetch"] == "performance":
    df = fetch_performance(department, (start_date, end_date), threshold)
    fig = plot_performance_trends(df)
    fname = f"{department}_Performance_{start_date[:7]}_{end_date[:7]}.png"
    render_plot_with_download(fig, "Performance Trends", fname)

elif config["fetch"] == "department_perf":
    df = fetch_department_performance(department)
    fig = plot_department_performance(df)
    fname = f"{department}_Department_Performance.png"
    render_plot_with_download(fig, "Department Performance", fname)

elif config["fetch"] == "attrition":
    df = fetch_attrition(department, start_date, end_date)
    fig = plot_attrition_rate(df)
    fname = f"{department}_Attrition_{start_date[:7]}_{end_date[:7]}.png"
    render_plot_with_download(fig, "Attrition Analysis", fname)

elif config["fetch"] == "load":
    df = fetch_department_load(department, start_date, end_date)
    fig = plot_department_load(df)
    fname = f"{department}_DeptLoad_{start_date[:7]}_{end_date[:7]}.png"
    render_plot_with_download(fig, "Department Load", fname)

elif config["fetch"] == "tenure":
    df = fetch_tenure(department)
    fig = plot_employee_tenure_ladder(df)
    fname = f"{department}_Tenure_Ladder.png"
    render_plot_with_download(fig, "Employee Tenure Ladder", fname)

elif config["fetch"] == "overlap":
    df = fetch_overlap(department)
    st.subheader("Project Overlap Detection")
    if df is not None and not df.empty:
        st.dataframe(df)
        fname = f"{department}_Project_Overlap.xlsx"
        download_as_excel(df, fname)
    else:
        st.info("No overlapping projects found.")

elif config["fetch"] == "timelines":
    df = fetch_timelines(department)
    fig = plot_employee_project_timelines(df)
    fname = f"{department}_Project_Timelines.png"
    render_plot_with_download(fig, "Employee Project Timelines", fname)
