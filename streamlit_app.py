import streamlit as st
from typing import Dict
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- THEME COLORS ---
PRIMARY_COLOR = '#00306B'  # Deep blue
BG_COLOR = '#F7F9FB'      # Very light gray/white
CARD_COLOR = '#FFFFFF'    # White for cards
TEXT_COLOR = '#00306B'    # Deep blue for text
ACCENT_COLOR = '#00306B'  # Deep blue for headers/buttons
BORDER_COLOR = '#BFCBDA'  # Light gray-blue for borders
YELLOW = '#FFD600'        # Yellow for branding

# --- AUTH ---
USERS = {
    'admin': 'admin123',
    'user': 'user123',
}

LOGO_PATH = os.path.abspath('image.png')
print('Logo exists:', os.path.exists(LOGO_PATH), '| Path:', LOGO_PATH)
APP_NAME = 'Yellow Jacket'
APP_SUBTITLE = 'Oil Well Management System'

# --- NAVIGATION ICONS ---
NAV_ICONS = [
    '🏠', '📄', '⬆️', '👤', '📊', '⚙️', '🚪'
]

# --- SETTINGS STATE ---
def get_settings():
    if 'settings' not in st.session_state:
        st.session_state['settings'] = {
            'Theme': 'Dark',
            'Language': 'English',
            'Notifications': True,
            'Auto-save': True
        }
    return st.session_state['settings']

# --- Fix login form button color and error handling ---
def login_form() -> bool:
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {BG_COLOR}; }}
        .stTextInput > div > div > input {{ color: {TEXT_COLOR}; background: #eaf1fb; }}
        .stButton > button {{ background: {PRIMARY_COLOR}; color: #fff; font-weight: bold; border-radius: 8px; }}
        </style>
    """, unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=200)
    st.title("Login to Yellow Jacket")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")
    if login_clicked:
        if username in USERS and USERS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
    return False

def sidebar_nav():
    # Custom sidebar styling
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{
            background-color: {BG_COLOR} !important;
            color: {TEXT_COLOR} !important;
            border-top-right-radius: 18px;
            border-bottom-right-radius: 18px;
            min-width: 270px;
        }}
        [data-testid="stSidebar"] .stRadio > div {{
            color: {TEXT_COLOR} !important;
        }}
        [data-testid="stSidebar"] .stRadio label span {{
            color: {ACCENT_COLOR} !important;
            font-weight: 600;
            font-size: 1.08rem;
        }}
        [data-testid="stSidebar"] .stRadio label div[data-testid="stMarkdownContainer"] {{
            display: flex;
            align-items: center;
            gap: 0.5em;
        }}
        [data-testid="stSidebar"] img {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 0.5em;
        }}
        [data-testid="stSidebar"] h2 {{
            text-align: center;
            margin-top: 0.2em;
            margin-bottom: 1.2em;
            color: {ACCENT_COLOR};
            font-size: 1.5rem;
            font-weight: bold;
            letter-spacing: 0.02em;
        }}
        [data-testid="stSidebar"] hr {{
            border: 1px solid {BORDER_COLOR};
            margin: 1.2em 0 0.7em 0;
        }}
        </style>
    """, unsafe_allow_html=True)
    nav_items = [
        'Dashboard', 'Job Logs', 'Upload Data', 'Users', 'Analytics', 'Settings', 'Logout'
    ]
    nav_icons = NAV_ICONS
    nav_labels = [f"{icon} {item}" for icon, item in zip(nav_icons, nav_items)]
    st.sidebar.image(LOGO_PATH, width=120)
    st.sidebar.markdown(f"<h2 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Menu</h2>", unsafe_allow_html=True)
    selected = st.sidebar.radio(
        'Navigation', nav_labels,
        index=nav_items.index(st.session_state.get('active_tab', 'Dashboard')),
        key='nav_radio_sidebar',
        label_visibility='collapsed'
    )
    st.session_state['active_tab'] = nav_items[nav_labels.index(selected)]
    # Move upload button to sidebar
    if st.session_state['active_tab'] == 'Dashboard':
        st.sidebar.markdown(f"<b>Quick Upload</b>", unsafe_allow_html=True)
        uploaded_file = st.sidebar.file_uploader("Upload Job Log File", type=["xlsx", "xls", "csv"], key="sidebar_upload")
        if uploaded_file is not None:
            st.session_state['sidebar_uploaded_file'] = uploaded_file
            st.sidebar.success("File uploaded! Go to 'Upload Data' to process.")

def main():
    st.set_page_config(page_title=APP_NAME, layout="wide")
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = 'Dashboard'
    if not st.session_state["authenticated"]:
        login_form()
        return
    st.markdown(f"<style>body {{ background: {BG_COLOR}; color: {TEXT_COLOR}; }}</style>", unsafe_allow_html=True)
    # --- Sidebar Navigation ---
    sidebar_nav()
    # --- Page Routing ---
    page_map = {
        'Dashboard': dashboard_page,
        'Job Logs': joblogs_page,
        'Upload Data': upload_page,
        'Users': users_page,
        'Analytics': analytics_page,
        'Settings': settings_page,
        'Logout': logout_page
    }
    # Render the selected page
    page_map[st.session_state['active_tab']]()

# --- DASHBOARD PAGE: Replace Job Logs table with upload section, remove white bar ---
def dashboard_page():
    st.title("Dashboard")
    st.write("Overview of your drilling operations and job logs.")
    col1, col2, col3, col4 = st.columns(4)
    for col, value, label, change, color in [
        (col1, '1,247', 'Total Job Logs', '+12.5%', 'green'),
        (col2, '28', 'Active Supervisors', '+2 this month', 'green'),
        (col3, '43', 'Pending Reviews', '-8.2%', 'red'),
        (col4, '892', 'Completed Jobs', '+15.3%', 'green'),
    ]:
        with col:
            st.markdown(f"<div style='background:{PRIMARY_COLOR};color:#fff;padding:1.2rem 1rem 0.7rem 1rem;border-radius:12px;box-shadow:0 2px 8px #0002;'><h2 style='margin:0;'>{value}</h2><div style='font-weight:600;'>{label}</div><div style='color:{color};font-size:0.9rem;font-weight:600;'>{change}</div></div>", unsafe_allow_html=True)
    # Remove the large <br> line and white bar
    # st.markdown("<br>", unsafe_allow_html=True)
    # --- Upload log file section ---
    st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1.5rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};margin-bottom:1.5rem;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Quick Upload</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Job Log File", type=["xlsx", "xls", "csv"], key="dashboard_upload")
    if uploaded_file is not None:
        st.session_state['sidebar_uploaded_file'] = uploaded_file
        st.session_state['uploaded_file_ready'] = True
        st.success("File uploaded! Go to 'Upload Data' to process.")
    st.markdown("</div>", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};'><h4 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Recent Activity</h4><div style='color:#555;'>Latest updates and system events</div><ul style='color:{TEXT_COLOR};margin-top:1rem;'><li>Job log JL-2024-001 uploaded by Mike Johnson</li><li>Supervisor Sarah Williams completed review</li><li>System backup completed</li><li>New user Robert Chen added</li></ul></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};'><h4 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Recent Error Logs</h4><div style='color:#555;'>Latest system errors and warnings</div><ul style='color:{TEXT_COLOR};margin-top:1rem;'><li><span style='color:red;'>[High]</span> Missing supervisor name in row 5 of well_data_batch_12.xlsx</li><li><span style='color:orange;'>[Medium]</span> Invalid zip code format in customer_update_jan15.xlsx</li><li><span style='color:green;'>[Resolved]</span> Data import issue fixed</li></ul></div>", unsafe_allow_html=True)

def joblogs_page():
    st.title("Job Logs")
    st.write("Manage and review all drilling operation logs.")
    data = [
        ["JL-2024-001", "Texas Oil Corporation", "Permian Basin Well #47", "Mike Johnson", "Texas, 79701", "Completed", "2024-01-15"],
        ["JL-2024-002", "Gulf Coast Energy", "Offshore Platform Alpha", "Sarah Williams", "Louisiana, 70112", "In Progress", "2024-01-14"],
        ["JL-2024-003", "Rocky Mountain Oil", "Bakken Shale Site 12", "Robert Chen", "North Dakota, 58801", "Under Review", "2024-01-13"],
    ]
    columns = ["Job ID", "Customer", "Well Name", "Supervisor", "Location", "Status", "Date"]
    df = pd.DataFrame(data, columns=columns)
    search = st.text_input("Search by customer, well name, supervisor...", key="joblogs_search")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    def status_badge(status):
        color = {"Completed": "#1abc9c", "In Progress": "#f1c40f", "Under Review": "#e74c3c"}.get(status, "#888")
        return f"<span style='background:{color};color:#fff;padding:0.3em 0.8em;border-radius:8px;font-size:0.95em;'>{status}</span>"
    st.markdown("<style>th, td {padding: 0.5em 1em !important;}</style>", unsafe_allow_html=True)
    table_html = "<table style='width:100%;background:{CARD_COLOR};border-radius:10px;overflow:hidden;'><thead><tr>"
    for col in columns:
        table_html += f"<th style='color:{ACCENT_COLOR};text-align:left;'>{col}</th>"
    table_html += "<th style='color:{ACCENT_COLOR};text-align:left;'>Actions</th></tr></thead><tbody>"
    for _, row in df.iterrows():
        table_html += "<tr>"
        for i, val in enumerate(row):
            if columns[i] == "Status":
                table_html += f"<td>{status_badge(val)}</td>"
            else:
                table_html += f"<td style='color:{TEXT_COLOR};'>{val}</td>"
        table_html += "<td><button style='background:{PRIMARY_COLOR};color:{ACCENT_COLOR};border:none;padding:0.3em 1em;border-radius:6px;cursor:pointer;'>...</button></td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.download_button("Export as Excel", df.to_csv(index=False).encode(), file_name="job_logs.csv", mime="text/csv", key="export_joblogs")

# --- UPLOAD PAGE: General Info as Job Summary cards (4 in a row, matching analytics style) ---
def upload_page():
    st.title("Upload Data")
    st.write("Import Excel sheets containing job logs and supervisor data.")
    uploaded_file = st.session_state.get('sidebar_uploaded_file', None)
    st.session_state['sheet_data'] = None
    st.session_state['sheet_name'] = None
    st.session_state['sheet_fields'] = None
    required_cols = [
        # Header fields (exact as in images)
        "Job Type:", "Start Date:", "End Date:", "FTS", "Ticket #:", "Co Rep:", "Co Rep Ph:",
        "Customer:", "Lease/Well#:", "Field/Block#:", "State:", "County:", "Rig:", "Casing:",
        "Motor Type:", "Motor Size:", "Mill Type:", "Mill Dressing:", "Extended Reach Tool:", "TOTAL # OF RUNS:",
        # Table columns (exact as in image)
        "Plug/Seat No.", "Tag Time", "Tag Plug/Seat Depth", "Drill Time (mins)", "Actual Plug/Seat Set Depth",
        "Plug/Seat Depth Difference", "Free Swivel Torque", "Circ. Pressure (PSI)", "Wellhead Pressure (PSI)",
        "Pump Rate (BPM)", "Return Rate (BPM)", "N2 Pump Rate (scfm)", "Weight on Bit", "Run In Weight (lbs)",
        "Pick Up Weight (lbs)", "RPMS", "Tag Joint Number", "Comments  (Motor Serial #, Sweep bbls, etc...)"
    ]
    upload_error = None
    all_sheets_data = []
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith("csv"):
                df = pd.read_csv(uploaded_file)
                df = df.dropna(axis=1, how='all')
                df = df.loc[:, df.notna().any()]
                all_sheets_data.append(("CSV File", df))
                st.success("CSV file uploaded and processed!")
            else:
                xls = pd.ExcelFile(uploaded_file)
                for sheet in xls.sheet_names:
                    raw_df = xls.parse(sheet, header=None)
                    header_row = None
                    for i, row in raw_df.iterrows():
                        if row.count() >= 3:
                            header_row = i
                            break
                    if header_row is not None:
                        df = pd.read_excel(uploaded_file, sheet_name=sheet, header=header_row)
                        df = df.dropna(axis=1, how='all')
                        df = df.loc[:, df.notna().any()]
                        all_sheets_data.append((sheet, df))
                    else:
                        st.warning(f"Could not detect data table in sheet: {sheet}")
                if all_sheets_data:
                    st.success(f"Processed {len(all_sheets_data)} sheet(s)!")
            if all_sheets_data:
                st.session_state['sheet_data'] = all_sheets_data[0][1]
                st.session_state['sheet_name'] = all_sheets_data[0][0]
                st.session_state['sheet_fields'] = list(all_sheets_data[0][1].columns)
            for sheet, df in all_sheets_data:
                st.markdown(f"<div style='margin-top:2rem;'><h4 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Sheet: {sheet}</h4></div>", unsafe_allow_html=True)
                if sheet.lower().startswith('general') or sheet.lower() == 'csv file':
                    # --- Inject summary cards (from screenshot, including Total Activities) ---
                    cards_html = """
                    <div style='display:flex;flex-wrap:wrap;gap:1.5rem 2.5rem;'>
                        <div style='background:#eaf1fb;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>👤</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Customer</span><br>
                            <span style='color:#222;font-size:1.15em;'>Mughees Khan</span>
                        </div>
                        <div style='background:#fffbe6;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>🎫</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Ticket #</span><br>
                            <span style='color:#222;font-size:1.15em;'>AE867384</span>
                        </div>
                        <div style='background:#e6fff7;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>🛠️</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Operation Type</span><br>
                            <span style='color:#222;font-size:1.15em;'>Drillout Operation</span>
                        </div>
                        <div style='background:#fbe6ff;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>⛽</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Well</span><br>
                            <span style='color:#222;font-size:1.15em;'>Well #1</span>
                        </div>
                        <div style='background:#e6f7ff;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>📍</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>County</span><br>
                            <span style='color:#222;font-size:1.15em;'>Dubai</span>
                        </div>
                        <div style='background:#eaf1fb;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>⏱️</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Duration</span><br>
                            <span style='color:#222;font-size:1.15em;'>7 Days</span>
                        </div>
                        <div style='background:#fffbe6;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>📅</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Start</span><br>
                            <span style='color:#222;font-size:1.15em;'>2025-06-12</span>
                        </div>
                        <div style='background:#e6fff7;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>📅</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>End</span><br>
                            <span style='color:#222;font-size:1.15em;'>2025-06-19</span>
                        </div>
                        <div style='background:#fbe6ff;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>🧑‍💼</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Supervisor</span><br>
                            <span style='color:#222;font-size:1.15em;'>Saif Khan</span>
                        </div>
                        <div style='background:#e6f7ff;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
                            <span style='font-size:1.5em;'>📋</span><br>
                            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Total Activities</span><br>
                            <span style='color:#222;font-size:1.15em;'>78<br><span style='color:green;font-size:0.95em;'>11.1 per day</span></span>
                        </div>
                    </div>
                    """
                    st.markdown(cards_html, unsafe_allow_html=True)
                    # (Removed original dynamic General Info cards)
                elif 'mill' in sheet.lower():
                    import random
                    st.markdown(f"<h2 style='color:{ACCENT_COLOR};margin-bottom:1rem;'>🔩 Mill Data (Sample)</h2>", unsafe_allow_html=True)
                    n_rows = 15
                    dummy_mill = pd.DataFrame({
                        'Plug/Seat No.': [i+1 for i in range(n_rows)],
                        'Tag Time': [f"{8+i//2:02d}:{30*(i%2):02d}" for i in range(n_rows)],
                        'Tag Plug/Seat Depth': [random.randint(9500, 11000) for _ in range(n_rows)],
                        'Drill Time (mins)': [random.randint(35, 55) for _ in range(n_rows)],
                        'Actual Plug/Seat Set Depth': [random.randint(9500, 11000) for _ in range(n_rows)],
                        'Comments': random.choices(['OK', 'Good', 'Check', 'Review', 'Replace', 'N/A'], k=n_rows)
                    })
                    st.dataframe(dummy_mill, use_container_width=True, hide_index=True)
                else:
                    st.markdown(f"<div style='background:{CARD_COLOR};border-radius:14px;padding:1.5rem 1rem 1rem 1rem;border:1.5px solid {PRIMARY_COLOR};box-shadow:0 2px 8px #00306b22;margin-bottom:2rem;'><h2 style='color:{ACCENT_COLOR};margin-bottom:1rem;'>Preview</h2>", unsafe_allow_html=True)
                    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            upload_error = str(e)
            st.error(f"Error reading file: {e}")
    else:
        st.info("No file uploaded. Please upload an Excel or CSV file.")
    # (Removed required columns info popup)

# --- ANALYTICS PAGE: Initial section as responsive grid of beautiful cards ---
def analytics_page():
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np
    import pandas as pd
    import json
    st.title("Analytics")
    st.write("Advanced Drilling Operations Analysis & Performance Tracking")
    job_info = {
        'customer_name': 'Mughees Khan',
        'ticket_number': 'AE867384',
        'job_type': 'Drillout Operation',
        'well_number': 'Well #1',
        'county': 'Dubai',
        'duration_days': 7,
        'date_started': '2025-06-12',
        'date_ended': '2025-06-19',
        'day_supervisor': 'Saif Khan',
    }
    ops_freq = {
        'total_activities': 78,
        'avg_activities_per_day': 11.1,
        'total_work_hours': 68.5,
        'avg_hours_per_day': 9.8,
    }
    efficiency = {
        'drilling_efficiency': 85,
        'safety_score': 98,
    }
    equipment_freq = {
        'deployment_success_rate': 83,
        'performance_distribution': {'excellent': 7, 'good': 2, 'poor': 1},
    }
    mill_perf = {
        'total_plugs_drilled': 10,
        'total_footage': 30,
        'avg_drill_time_mins': 42.3,
        'efficiency_rating': 'High',
        'success_rate': 100,
    }
    ct_perf = {
        'total_ct_operations': 5,
        'depth_accuracy': 95.5,
        'avg_ct_drill_time': 36.8,
        'efficiency_rating': 'Excellent',
    }
    daily_breakdown = [
        {'day': f'Day {i+1}', 'date': f'2025-06-{12+i}', 'activities': np.random.randint(8, 15), 'work_hours': np.random.uniform(8, 12), 'downtime': np.random.uniform(0, 2), 'mill_operations': np.random.randint(1, 3), 'ct_operations': np.random.randint(0, 2), 'equipment': ['FT3', 'FT6'] if i%2==0 else ['FT1', 'FT2']} for i in range(7)
    ]
    equipment_usage = {
        'FT3': {'tool_type': 'Mill', 'usage_count': 5, 'success_rate': 98, 'avg_deployment_time': 1.2, 'maintenance_due': False},
        'FT6': {'tool_type': 'CT', 'usage_count': 4, 'success_rate': 92, 'avg_deployment_time': 1.5, 'maintenance_due': True},
        'FT1': {'tool_type': 'Mill', 'usage_count': 3, 'success_rate': 85, 'avg_deployment_time': 1.1, 'maintenance_due': False},
        'FT2': {'tool_type': 'CT', 'usage_count': 2, 'success_rate': 80, 'avg_deployment_time': 1.3, 'maintenance_due': False},
    }
    recommendations = [
        "✅ Excellent drilling performance with 42.3 min average - maintain current operational parameters",
        "🔧 2 tools (FT3, FT6) require maintenance review before next deployment",
        "🎯 High drilling efficiency achieved (88%) - consider sharing best practices with other crews",
        "💡 CT operations showing excellent efficiency (36.8 min avg) - optimize for future jobs",
        "🛡️ Maintain excellent safety record with continued JSA compliance and observation protocols"
    ]
    # --- Job Summary and KPIs as a single HTML block (matches your provided HTML) ---
    # Only show Total Activities card
    total_activities_card = """
    <div style='display:flex;flex-wrap:wrap;gap:1.5rem 2.5rem;'>
        <div style='background:#e6f7ff;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
            <span style='font-size:1.5em;'>📋</span><br>
            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Total Activities</span><br>
            <span style='color:#222;font-size:1.15em;'>78<br><span style='color:green;font-size:0.95em;'>11.1 per day</span></span>
        </div>
        <div style='background:#eaf1fb;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
            <span style='font-size:1.5em;'>⏰</span><br>
            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Work Hours</span><br>
            <span style='color:#222;font-size:1.15em;'>68.5<br><span style='color:green;font-size:0.95em;'>9.8 per day</span></span>
        </div>
        <div style='background:#fffbe6;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
            <span style='font-size:1.5em;'>⚡</span><br>
            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Drilling Efficiency</span><br>
            <span style='color:#222;font-size:1.15em;'>85%<br><span style='color:green;font-size:0.95em;'>performance rating</span></span>
        </div>
        <div style='background:#e6fff7;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
            <span style='font-size:1.5em;'>🔧</span><br>
            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Equipment Success</span><br>
            <span style='color:#222;font-size:1.15em;'>83%<br><span style='color:green;font-size:0.95em;'>deployment success</span></span>
        </div>
        <div style='background:#fbe6ff;border-radius:12px;padding:1.1em 1.5em;margin:0.7em 0 0.7em 0;border:2px solid #00306B;box-shadow:0 1px 6px #00306b22;min-width:260px;max-width:400px;flex:1;'>
            <span style='font-size:1.5em;'>🛡️</span><br>
            <span style='color:#00306B;font-weight:700;font-size:1.1em;'>Safety Score</span><br>
            <span style='color:#222;font-size:1.15em;'>98<br><span style='color:green;font-size:0.95em;'>out of 100</span></span>
        </div>
    </div>
    """
    st.markdown(total_activities_card, unsafe_allow_html=True)
    # --- Drilling Performance ---
    st.header("🚀 Drilling Performance Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚙️ Mill Operations")
        mill_col1, mill_col2 = st.columns(2)
        with mill_col1:
            st.metric("Plugs Drilled", mill_perf['total_plugs_drilled'], f"{mill_perf['total_footage']} ft total")
        with mill_col2:
            st.metric("Avg Drill Time", f"{mill_perf['avg_drill_time_mins']} min", mill_perf['efficiency_rating'])
    with col2:
        st.subheader("🔄 CT Operations")
        ct_col1, ct_col2 = st.columns(2)
        with ct_col1:
            st.metric("CT Operations", ct_perf['total_ct_operations'], f"{ct_perf['depth_accuracy']}% accuracy")
        with ct_col2:
            st.metric("Avg CT Time", f"{ct_perf['avg_ct_drill_time']} min", ct_perf['efficiency_rating'])
    # --- Drilling Performance Charts ---
    col1, col2 = st.columns(2)
    with col1:
        drill_times = [42.3 - i*1.2 + np.random.normal(0, 2) for i in range(10)]
        plug_numbers = list(range(1, 11))
        fig_drill_times = px.line(x=plug_numbers, y=drill_times, title='Drill Time Progression by Plug', labels={'x': 'Plug Number', 'y': 'Drill Time (minutes)'}, markers=True)
        fig_drill_times.update_traces(line_color='#2a5298', marker_size=8)
        fig_drill_times.add_hline(y=np.mean(drill_times), line_dash="dash", annotation_text=f"Average: {np.mean(drill_times):.1f} min")
        st.plotly_chart(fig_drill_times, use_container_width=True)
    with col2:
        efficiency_data = {
            'Operation Type': ['Mill Operations', 'CT Operations', 'Industry Standard'],
            'Efficiency Score': [mill_perf['success_rate'], ct_perf['depth_accuracy'], 85],
            'Color': ['Mill', 'CT', 'Standard']
        }
        fig_efficiency = px.bar(efficiency_data, x='Operation Type', y='Efficiency Score', title='Operation Efficiency Comparison', color='Color', color_discrete_map={'Mill': '#2a5298', 'CT': '#28a745', 'Standard': '#6c757d'})
        fig_efficiency.update_layout(showlegend=False)
        st.plotly_chart(fig_efficiency, use_container_width=True)
    # --- Operational Frequency ---
    st.header("📈 Operational Frequency Analysis")
    col1, col2 = st.columns(2)
    daily_data = pd.DataFrame(daily_breakdown)
    with col1:
        fig_activities = go.Figure()
        fig_activities.add_trace(go.Bar(name='Total Activities', x=daily_data['day'], y=daily_data['activities'], marker_color='#2a5298', opacity=0.7))
        fig_activities.add_trace(go.Scatter(name='Mill Operations', x=daily_data['day'], y=daily_data['mill_operations'], mode='lines+markers', line=dict(color='#dc3545', width=3), marker=dict(size=8)))
        fig_activities.add_trace(go.Scatter(name='CT Operations', x=daily_data['day'], y=daily_data['ct_operations'], mode='lines+markers', line=dict(color='#28a745', width=3), marker=dict(size=8)))
        fig_activities.update_layout(title='Daily Activities & Drilling Operations', xaxis_title='Day', yaxis_title='Count', legend=dict(x=0, y=1))
        st.plotly_chart(fig_activities, use_container_width=True)
    with col2:
        fig_hours = go.Figure()
        fig_hours.add_trace(go.Bar(name='Work Hours', x=daily_data['day'], y=daily_data['work_hours'], marker_color='#2a5298'))
        fig_hours.add_trace(go.Bar(name='Downtime', x=daily_data['day'], y=daily_data['downtime'], marker_color='#dc3545'))
        fig_hours.update_layout(title='Daily Work Hours vs Downtime', xaxis_title='Day', yaxis_title='Hours', barmode='stack')
        st.plotly_chart(fig_hours, use_container_width=True)
    # --- Equipment Analysis ---
    st.header("🔧 Equipment Utilization Analysis")
    col1, col2 = st.columns(2)
    eq_df = pd.DataFrame([
        {'Tool': tool, 'Tool Type': info['tool_type'], 'Usage Count': info['usage_count'], 'Success Rate': info['success_rate'], 'Avg Deployment Time': info['avg_deployment_time'], 'Maintenance Due': info['maintenance_due']} for tool, info in equipment_usage.items()
    ])
    with col1:
        fig_eq_usage = px.bar(eq_df, x='Tool', y='Usage Count', title='Equipment Usage Frequency', color='Success Rate', color_continuous_scale='RdYlGn', hover_data=['Tool Type', 'Avg Deployment Time'])
        st.plotly_chart(fig_eq_usage, use_container_width=True)
    with col2:
        fig_performance = px.pie(values=list(equipment_freq['performance_distribution'].values()), names=list(equipment_freq['performance_distribution'].keys()), title='Equipment Performance Distribution', color_discrete_map={'excellent': '#28a745', 'good': '#17a2b8', 'poor': '#dc3545'})
        st.plotly_chart(fig_performance, use_container_width=True)
    st.subheader("🔍 Equipment Details & Maintenance Status")
    eq_display = eq_df.copy()
    def get_status_emoji(row):
        if row['Maintenance Due']:
            return "🔴 Maintenance Required"
        elif row['Success Rate'] >= 95:
            return "🟢 Excellent"
        elif row['Success Rate'] >= 85:
            return "🟡 Good"
        else:
            return "🟠 Needs Attention"
    eq_display['Status'] = eq_display.apply(get_status_emoji, axis=1)
    eq_display['Success Rate'] = eq_display['Success Rate'].apply(lambda x: f"{x:.0f}%")
    eq_display['Avg Deployment Time'] = eq_display['Avg Deployment Time'].apply(lambda x: f"{x:.1f}h")
    st.dataframe(eq_display[['Tool', 'Tool Type', 'Usage Count', 'Success Rate', 'Avg Deployment Time', 'Status']], use_container_width=True)
    # --- Detailed Daily Breakdown ---
    st.header("📅 Detailed Daily Operations")
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "⏱️ Drilling Timeline", "🛠️ Equipment Schedule"])
    with tab1:
        daily_detailed = daily_data.copy()
        daily_detailed['Efficiency'] = (daily_detailed['activities'] / daily_detailed['work_hours']).round(2)
        daily_detailed['Equipment Count'] = daily_detailed['equipment'].apply(len)
        daily_detailed['Total Drilling Ops'] = daily_detailed['mill_operations'] + daily_detailed['ct_operations']
        st.dataframe(daily_detailed[['day', 'date', 'activities', 'work_hours', 'downtime', 'mill_operations', 'ct_operations', 'Total Drilling Ops', 'Equipment Count', 'Efficiency']], use_container_width=True)
    with tab2:
        fig_drilling_timeline = go.Figure()
        fig_drilling_timeline.add_trace(go.Bar(name='Mill Operations', x=daily_data['day'], y=daily_data['mill_operations'], marker_color='#dc3545', width=0.4, offset=-0.2))
        fig_drilling_timeline.add_trace(go.Bar(name='CT Operations', x=daily_data['day'], y=daily_data['ct_operations'], marker_color='#28a745', width=0.4, offset=0.2))
        fig_drilling_timeline.update_layout(title='Drilling Operations Timeline', xaxis_title='Day', yaxis_title='Number of Operations', barmode='group', height=400)
        st.plotly_chart(fig_drilling_timeline, use_container_width=True)
    with tab3:
        equipment_schedule = []
        for day_data in daily_breakdown:
            for equipment in day_data.get('equipment', []):
                equipment_schedule.append({'Day': day_data['day'], 'Date': day_data['date'], 'Equipment': equipment, 'Work Hours': day_data['work_hours']})
        if equipment_schedule:
            eq_schedule_df = pd.DataFrame(equipment_schedule)
            fig_eq_schedule = px.density_heatmap(eq_schedule_df, x='Day', y='Equipment', title='Equipment Usage Schedule', color_continuous_scale='Blues')
            st.plotly_chart(fig_eq_schedule, use_container_width=True)
            eq_utilization = eq_schedule_df.groupby('Equipment').agg({'Day': 'count', 'Work Hours': 'sum'}).rename(columns={'Day': 'Days Used', 'Work Hours': 'Total Hours'})
            st.subheader("Equipment Utilization Summary")
            st.dataframe(eq_utilization, use_container_width=True)
        else:
            st.info("No equipment schedule data available")
    # --- Recommendations ---
    st.header("💡 AI-Powered Recommendations")
    for i, rec in enumerate(recommendations, 1):
        if 'excellent' in rec.lower() or 'maintain' in rec.lower():
            rec_type = "success-metric"
            icon = "✅"
        elif 'maintenance' in rec.lower() or 'require' in rec.lower():
            rec_type = "warning-metric"  
            icon = "⚠️"
        elif 'efficiency' in rec.lower() or 'optimize' in rec.lower():
            rec_type = "drill-metric"
            icon = "🎯"
        elif 'safety' in rec.lower():
            rec_type = "success-metric"
            icon = "🛡️"
        else:
            rec_type = "metric-card"
            icon = "💡"
        st.markdown(f"""
        <div class="metric-card {rec_type}" style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #2a5298; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <h4 style="margin: 0; color: #333;">{icon} Recommendation {i}</h4>
            <p style="margin: 0.5rem 0 0 0; color: #666;">{rec}</p>
        </div>
        """, unsafe_allow_html=True)
    # --- Advanced Analytics ---
    st.header("📊 Advanced Drilling Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚡ Drilling Efficiency Trends")
        days = list(range(1, 8))
        efficiency_trend = [85 + i*0.5 + np.random.normal(0, 1.5) for i in days]
        fig_efficiency_trend = go.Figure()
        fig_efficiency_trend.add_trace(go.Scatter(x=days, y=efficiency_trend, mode='lines+markers', name='Efficiency %', line=dict(color='#2a5298', width=3), marker=dict(size=8)))
        fig_efficiency_trend.add_hline(y=np.mean(efficiency_trend), line_dash="dash", line_color="red", annotation_text=f"Average: {np.mean(efficiency_trend):.1f}%")
        fig_efficiency_trend.update_layout(title='Daily Drilling Efficiency', xaxis_title='Day', yaxis_title='Efficiency %', yaxis_range=[80, 95])
        st.plotly_chart(fig_efficiency_trend, use_container_width=True)
    with col2:
        st.subheader("💰 Cost Efficiency Analysis")
        cost_data = {'Category': ['Equipment', 'Labor', 'Materials', 'Overhead'], 'Budgeted': [15000, 25000, 8000, 12000], 'Actual': [14200, 23800, 7600, 11400], 'Variance': [800, 1200, 400, 600]}
        cost_df = pd.DataFrame(cost_data)
        fig_cost = go.Figure()
        fig_cost.add_trace(go.Bar(name='Budgeted', x=cost_df['Category'], y=cost_df['Budgeted'], marker_color='lightblue'))
        fig_cost.add_trace(go.Bar(name='Actual', x=cost_df['Category'], y=cost_df['Actual'], marker_color='darkblue'))
        fig_cost.update_layout(title='Budget vs Actual Costs', xaxis_title='Cost Category', yaxis_title='Amount (USD)', barmode='group')
        st.plotly_chart(fig_cost, use_container_width=True)
        total_savings = cost_df['Variance'].sum()
        st.metric(label="Total Cost Savings", value=f"${total_savings:,}", delta=f"{(total_savings/cost_df['Budgeted'].sum()*100):.1f}% under budget")
    # --- Export Section ---
    st.header("📤 Export & Reports")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(label="Download Drilling Report (JSON)", data=json.dumps({'Job Information': job_info, 'Drilling Performance': {'Mill Operations': mill_perf, 'CT Operations': ct_perf, 'Overall Efficiency': efficiency['drilling_efficiency']}, 'Key Metrics': {'Total Activities': ops_freq['total_activities'], 'Total Work Hours': ops_freq['total_work_hours'], 'Equipment Success Rate': equipment_freq['deployment_success_rate'], 'Safety Score': efficiency['safety_score']}, 'Equipment Status': equipment_usage, 'Recommendations': recommendations}, indent=2), file_name=f"YJOS_Drilling_Report_{job_info['ticket_number']}.json", mime="application/json")
    with col2:
        daily_csv = pd.DataFrame(daily_breakdown)
        st.download_button(label="Download Daily Operations CSV", data=daily_csv.to_csv(index=False), file_name=f"YJOS_Daily_Operations_{job_info['ticket_number']}.csv", mime="text/csv")
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🛠️ YJOS Drillout Analytics Dashboard | Advanced Drilling Operations Intelligence</p>
        <p>📧 Contact: drilling-analytics@yjos.com | 📞 Support: 1-800-YJOS-DRILL</p>
        <p>Specialized for Mill Operations, CT Drilling, and Equipment Optimization</p>
    </div>
    """, unsafe_allow_html=True)

def settings_page():
    st.title("Settings")
    st.write("Configure application settings and preferences.")
    settings = get_settings()
    with st.form("settings_form"):
        theme = st.selectbox("Theme", ["Dark", "Light"], index=0 if settings['Theme']=="Dark" else 1)
        language = st.selectbox("Language", ["English", "Spanish"], index=0 if settings['Language']=="English" else 1)
        notifications = st.checkbox("Enable Notifications", value=settings['Notifications'])
        autosave = st.checkbox("Enable Auto-save", value=settings['Auto-save'])
        submitted = st.form_submit_button("Save Settings")
        if submitted:
            settings['Theme'] = theme
            settings['Language'] = language
            settings['Notifications'] = notifications
            settings['Auto-save'] = autosave
            st.session_state['settings'] = settings
            st.success("Settings updated!")
    st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};margin-top:1rem;'><h4 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Current Settings</h4>", unsafe_allow_html=True)
    st.json(settings)
    st.markdown(f"<h4 style='color:{ACCENT_COLOR};'>Change Password</h4>", unsafe_allow_html=True)
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password", key="current_password")
        new_password = st.text_input("New Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")
        submitted = st.form_submit_button("Change Password")
        if submitted:
            if current_password == USERS[st.session_state["username"]]:
                if new_password == confirm_password:
                    USERS[st.session_state["username"]] = new_password
                    st.success("Password changed successfully!")
                else:
                    st.error("New passwords do not match.")
            else:
                st.error("Incorrect current password.")

def users_page():
    st.title("User Management")
    st.write("Manage system users, roles, and permissions.")
    user_data = {
        "Username": ["admin", "user", "sarah", "mike"],
        "Role": ["Admin", "Supervisor", "Supervisor", "Operator"],
        "Department": ["IT", "Field Ops", "Field Ops", "Maintenance"],
        "Status": ["Active", "Active", "Inactive", "Active"],
        "Jobs Completed": [120, 87, 0, 45],
        "Last Active": ["2024-01-15", "2024-01-14", "2023-12-30", "2024-01-13"]
    }
    df = pd.DataFrame(user_data)
    st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};margin-top:1rem;'><h4 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Users</h4>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{ACCENT_COLOR};'>Add New User</h4>", unsafe_allow_html=True)
    with st.form("add_user_form"):
        new_username = st.text_input("Username", key="add_user_username")
        new_role = st.selectbox("Role", ["Admin", "Supervisor", "Operator"], key="add_user_role")
        new_dept = st.text_input("Department", key="add_user_dept")
        new_status = st.selectbox("Status", ["Active", "Inactive"], key="add_user_status")
        new_jobs = st.number_input("Jobs Completed", min_value=0, value=0, key="add_user_jobs")
        new_last_active = st.date_input("Last Active", key="add_user_last_active")
        submitted = st.form_submit_button("Add User")
        if submitted:
            st.success(f"User '{new_username}' added (not saved in prototype)")

def logout_page():
    st.title("Logout")
    st.write("Log out of the application.")
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        if "username" in st.session_state:
            del st.session_state["username"]
        st.rerun()

if __name__ == "__main__":
    main() 
