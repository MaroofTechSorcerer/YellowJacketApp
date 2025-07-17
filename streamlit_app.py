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

# --- Fix visibility for all cards, buttons, and text ---
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
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1.5rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};margin-bottom:1.5rem;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Quick Actions</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#222;'>Common tasks and operations</div>", unsafe_allow_html=True)
    # Upload button as file uploader
    upload_col, analytics_col = st.columns([1,1])
    with upload_col:
        uploaded_file = st.file_uploader("Upload Job Log File", type=["xlsx", "xls", "csv"], key="dashboard_upload")
        if uploaded_file is not None:
            st.session_state['sidebar_uploaded_file'] = uploaded_file
            st.success("File uploaded! Go to 'Upload Data' to process.")
    with analytics_col:
        st.button("👁 View Analytics", key="dashboard_view_analytics", disabled=True)
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
    missing_required = []
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
            # Store the first sheet for analytics
            if all_sheets_data:
                st.session_state['sheet_data'] = all_sheets_data[0][1]
                st.session_state['sheet_name'] = all_sheets_data[0][0]
                st.session_state['sheet_fields'] = list(all_sheets_data[0][1].columns)
                # Check for missing required columns
                missing_required = [col for col in required_cols if col not in all_sheets_data[0][1].columns]
                if missing_required:
                    st.error(f"Missing required columns: {', '.join(missing_required)}")
            # Scorecard style summary for each sheet
            for sheet, df in all_sheets_data:
                st.markdown(f"<h4 style='color:{ACCENT_COLOR};margin-top:1.5rem;'>Sheet: {sheet}</h4>", unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Rows", len(df))
                with col2:
                    st.metric("Columns", len(df.columns))
                with col3:
                    st.metric("Filled Cells", int(df.count().sum()))
                with col4:
                    st.metric("Blank Cells", int(df.isna().sum().sum()))
        except Exception as e:
            upload_error = str(e)
            st.error(f"Error reading file: {e}")
    else:
        st.info("No file uploaded. Please upload an Excel or CSV file.")
    st.info("Required Excel columns (for full job log analytics): " + ', '.join(required_cols))

def analytics_page():
    import altair as alt
    st.title("Analytics")
    st.write("Performance insights and operational analytics.")
    # Overall project metrics only
    import random
    metrics = [
        ("Total Jobs", random.randint(1000, 2000)),
        ("Completed Jobs", random.randint(800, 1200)),
        ("Error Rate (%)", round(random.uniform(0.5, 5.0), 2)),
        ("Jobs This Month", random.randint(50, 150)),
    ]
    cols = st.columns(4)
    for i, (label, value) in enumerate(metrics):
        with cols[i % 4]:
            st.markdown(f"<div style='background:{PRIMARY_COLOR};color:#fff;padding:1.2rem 1rem 0.7rem 1rem;border-radius:12px;box-shadow:0 2px 8px #0002;'><h2 style='margin:0;'>{value}</h2><div style='font-weight:600;'>{label}</div></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)
    # Example bar chart with random data (overall jobs by month)
    chart_data = pd.DataFrame({
        'Month': [f"2024-{i+1:02d}" for i in range(6)],
        'Jobs Completed': [random.randint(50, 200) for _ in range(6)]
    })
    st.subheader("Jobs Completed by Month")
    bar = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X("Month:N"),
        y=alt.Y("Jobs Completed:Q"),
        tooltip=["Month", "Jobs Completed"]
    )
    st.altair_chart(bar, use_container_width=True)
    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)
    # Download overall report
    st.markdown("<b>Download Overall Report:</b>", unsafe_allow_html=True)
    st.download_button("Download CSV", chart_data.to_csv(index=False).encode(), file_name="overall_report.csv", mime="text/csv", key="download_overall_csv")

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
    st.markdown("<hr>")
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
