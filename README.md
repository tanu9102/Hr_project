# HR Analytics Dashboard

This project covers essential HR metrics using Python, SQL, and Streamlit. It features an interactive dashboard to monitor employee performance, analyze attrition trends, assess department workload, and detect project overlaps—enabling smart, data-driven HR decisions.
This is an **HR Analytics Dashboard** built using **Streamlit** and **Plotly** for visualizing key HR metrics and trends, such as performance trends, department performance, attrition analysis, department load, employee tenure ladder, project overlap, and employee project timelines.

The dashboard allows HR teams and managers to analyze data from different departments, track performance, and gain insights into employee attrition and workload.

## Features

- **Performance Trends**: Visualize trends in employee performance over a selected date range.
- **Department Performance**: Analyze performance metrics for each department.
- **Attrition Analysis**: Explore the attrition rate for employees within a given date range.
- **Department Load**: Understand department workload trends over time.
- **Employee Tenure Ladder**: Visualize employee tenure distribution within the company.
- **Project Overlap**: Detect overlapping projects and identify potential conflicts across employees.
- **Employee Project Timelines**: Visualize the timelines for employee projects.

## Technologies Used

- **Python** (3.x)
- **Streamlit**: For building the interactive dashboard.
- **Plotly**: For creating interactive plots and visualizations.
- **Pandas**: For data manipulation and analysis.
- **SQLite** (or any other database backend) for storing and fetching HR data.

## Installation

To run this project locally, follow the instructions below.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git https://github.com/saurabhingle/HrInsights.git
cd Hr_Dashboard
```

### 2. Set Up Virtual Environment


Create and activate a virtual environment to isolate project dependencies.
```bash
python -m venv venv
```

* On **Windows**, activate the virtual environment with:

  ```bash
  .\venv\Scripts\activate
  ```

* On **Mac/Linux**, activate it with:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python libraries from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Run Database Setup

After setting up the virtual environment and installing dependencies, you'll need to run the database setup file to set up the database.

```bash
python db/database_setup.py
```

### 5. Run Index Creation

Once the database is set up, run the index creation script to ensure optimal performance.

```bash
python db/index_creation.py
```

### 6. Run the Dashboard

To launch the HR Analytics Dashboard, run the following command:

```bash
streamlit run app.py
```

This will start the Streamlit app on your local server, and you can access it via `http://localhost:8501` in your browser.

