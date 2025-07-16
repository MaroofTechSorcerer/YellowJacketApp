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
    '🏠', '📄', '⬆️', '⬇️', '👤', '📊', '⚠️', '⚙️', '🚪'
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

def top_nav():
    nav_items = [
        'Dashboard', 'Job Logs', 'Upload Data', 'Download Reports', 'Users', 'Analytics', 'Error Logs', 'Settings', 'Logout'
    ]
    nav_icons = NAV_ICONS
    nav_labels = [f"{icon} {item}" for icon, item in zip(nav_icons, nav_items)]
    # Adjust column ratio for better balance
    cols = st.columns([1, 7])
    with cols[0]:
        if os.path.exists(LOGO_PATH):
            # Use st.image for correct file serving
            st.image(LOGO_PATH, width=150)
        else:
            st.warning(f"Logo not found at: {LOGO_PATH}")
    with cols[1]:
        selected = st.radio(
            '', nav_labels,
            index=nav_items.index(st.session_state.get('active_tab', 'Dashboard')),
            horizontal=True,
            key='nav_radio',
            label_visibility='collapsed'
        )
        st.session_state['active_tab'] = nav_items[nav_labels.index(selected)]

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
    # --- Top Navigation ---
    top_nav()
    # --- Page Routing ---
    page_map = {
        'Dashboard': dashboard_page,
        'Job Logs': joblogs_page,
        'Upload Data': upload_page,
        'Download Reports': download_page,
        'Users': users_page,
        'Analytics': analytics_page,
        'Error Logs': errorlogs_page,
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
    st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1.5rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};margin-bottom:1.5rem;'><h3 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Quick Actions</h3><div style='color:#222;'>Common tasks and operations</div><div style='display:flex;gap:2rem;margin-top:1rem;'><button style='background:{PRIMARY_COLOR};color:#fff;padding:0.7rem 2rem;border:none;border-radius:8px;font-weight:bold;font-size:1rem;cursor:pointer;'>⬆ Upload Job Log File</button><button style='background:#E6EEF7;color:{PRIMARY_COLOR};padding:0.7rem 2rem;border:none;border-radius:8px;font-weight:bold;font-size:1rem;cursor:pointer;'>👁 View Analytics</button></div></div>", unsafe_allow_html=True)
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
    uploaded_file = st.file_uploader("Click to upload files or drag and drop", type=["xlsx", "xls", "csv"], key="upload_data_file")
    st.session_state['sheet_data'] = None
    st.session_state['sheet_name'] = None
    st.session_state['sheet_fields'] = None
    required_cols = [
        "Customer Name", "State", "Zip Code", "Supervisor Name", "Well Name", "Date",
        "Materials Used", "Tools Used", "Observations", "Status"
    ]
    upload_error = None
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith("csv"):
                df = pd.read_csv(uploaded_file)
                st.session_state['sheet_data'] = df
                st.session_state['sheet_name'] = 'CSV File'
                st.session_state['sheet_fields'] = list(df.columns)
                st.success("CSV file uploaded successfully!")
            else:
                xls = pd.ExcelFile(uploaded_file)
                sheet_names = xls.sheet_names
                sheet = st.selectbox("Select sheet to analyze", sheet_names, key="sheet_select")
                raw_df = xls.parse(sheet, header=None)
                # Try to find the first row with at least 3 non-null values as header
                header_row = None
                for i, row in raw_df.iterrows():
                    if row.count() >= 3:
                        header_row = i
                        break
                if header_row is not None:
                    df = pd.read_excel(uploaded_file, sheet_name=sheet, header=header_row)
                    st.session_state['sheet_data'] = df
                    st.session_state['sheet_name'] = sheet
                    st.session_state['sheet_fields'] = list(df.columns)
                    st.success(f"Sheet '{sheet}' loaded successfully! Header row: {header_row+1}")
                    st.dataframe(df.head(20), use_container_width=True)
                else:
                    upload_error = "Could not automatically detect the data table in this sheet."
                    st.error(upload_error)
        except Exception as e:
            upload_error = str(e)
            st.error(f"Error reading file: {e}")
    else:
        st.info("No file uploaded. Please upload an Excel or CSV file.")
    # Remove HTML line for required columns, just show as text
    st.info("Required Excel columns (for full job log analytics): " + ', '.join(required_cols))
    if upload_error:
        if 'error_logs' not in st.session_state:
            st.session_state['error_logs'] = []
        st.session_state['error_logs'].append({
            'Error ID': f'ERR-UPLOAD-{len(st.session_state["error_logs"])+1}',
            'Type': 'High',
            'Message': upload_error,
            'Date': pd.Timestamp.now().strftime('%Y-%m-%d'),
            'Status': 'Open'
        })

def download_page():
    st.title("Download Reports")
    st.write("Generate and download comprehensive reports.")
    from datetime import date
    report_data = {
        "Job ID": ["JL-2024-001", "JL-2024-002"],
        "Customer": ["Texas Oil Corporation", "Gulf Coast Energy"],
        "Supervisor": ["Mike Johnson", "Sarah Williams"],
        "Status": ["Completed", "In Progress"],
        "Date": ["2024-01-15", "2024-01-14"]
    }
    df = pd.DataFrame(report_data)
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date(2024, 1, 1), key="report_start_date")
    with col2:
        end_date = st.date_input("End Date", value=date(2024, 1, 31), key="report_end_date")
    report_type = st.selectbox("Select Report Type", ["Job Summary", "Supervisor Performance", "Material Usage"], key="report_type")
    filtered_df = df[(df["Date"] >= str(start_date)) & (df["Date"] <= str(end_date))]
    st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};margin-top:1rem;'><h4 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Report Preview</h4>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown("<b>Download as:</b>", unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3)
    with col3:
        st.download_button("Excel", filtered_df.to_csv(index=False).encode(), file_name="report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="download_excel")
    with col4:
        st.download_button("CSV", filtered_df.to_csv(index=False).encode(), file_name="report.csv", mime="text/csv", key="download_csv")
    with col5:
        st.button("PDF (coming soon)", key="download_pdf", disabled=True)

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

def analytics_page():
    import altair as alt
    st.title("Analytics")
    st.write("Performance insights and operational analytics.")
    df = st.session_state.get('sheet_data', None)
    sheet_name = st.session_state.get('sheet_name', None)
    fields = st.session_state.get('sheet_fields', None)
    if df is not None and fields is not None:
        st.subheader(f"Analytics from {sheet_name}")
        # Clean up field names for selection, skip all-NaN or single-unique columns
        clean_fields = [str(f).strip() for f in fields if df[f].dropna().nunique() > 1]
        if not clean_fields:
            st.warning("No suitable fields for analytics in this sheet.")
            return
        selected_field = st.selectbox("Select field for analytics", clean_fields, key="analytics_field")
        if selected_field:
            col_data = df[selected_field].dropna()
            st.write(f"**Field type:** {col_data.dtype}")
            try:
                # Numeric: summary, bar, line
                if pd.api.types.is_numeric_dtype(col_data):
                    st.write("**Summary statistics:**")
                    st.write(col_data.describe())
                    chart_data = col_data.value_counts().reset_index()
                    chart_data.columns = ["Value", "Count"]
                    if len(chart_data) > 1:
                        bar = alt.Chart(chart_data).mark_bar().encode(
                            x=alt.X("Value:O", title=selected_field),
                            y=alt.Y("Count:Q"),
                            tooltip=["Value", "Count"]
                        )
                        st.altair_chart(bar, use_container_width=True)
                    else:
                        st.info("Not enough data for a bar chart.")
                # Categorical: bar, pie
                elif pd.api.types.is_object_dtype(col_data) or pd.api.types.is_categorical_dtype(col_data):
                    value_counts = col_data.value_counts().head(20)
                    st.write("**Top 20 value counts:**")
                    st.dataframe(value_counts)
                    chart_data = value_counts.reset_index()
                    chart_data.columns = ["Category", "Count"]
                    if len(chart_data) > 1:
                        bar = alt.Chart(chart_data).mark_bar().encode(
                            x=alt.X("Category:N", sort="-y"),
                            y=alt.Y("Count:Q"),
                            tooltip=["Category", "Count"]
                        )
                        st.altair_chart(bar, use_container_width=True)
                        pie = alt.Chart(chart_data).mark_arc().encode(
                            theta=alt.Theta(field="Count", type="quantitative"),
                            color=alt.Color(field="Category", type="nominal"),
                            tooltip=["Category", "Count"]
                        )
                        st.altair_chart(pie, use_container_width=True)
                    else:
                        st.info("Not enough data for a chart.")
                # Datetime: time series
                elif pd.api.types.is_datetime64_any_dtype(col_data):
                    st.write("**Time series:**")
                    ts = col_data.value_counts().sort_index().reset_index()
                    ts.columns = ["Date", "Count"]
                    if len(ts) > 1:
                        line = alt.Chart(ts).mark_line().encode(
                            x=alt.X("Date:T"),
                            y=alt.Y("Count:Q"),
                            tooltip=["Date", "Count"]
                        )
                        st.altair_chart(line, use_container_width=True)
                    else:
                        st.info("Not enough data for a time series chart.")
                else:
                    st.warning("This field type is not directly visualizable. Please select another field.")
            except Exception as e:
                st.warning(f"Could not plot chart for this field: {e}")
        st.markdown("---")
        st.markdown("**Preview of data used for analytics:**")
        st.dataframe(df.head(20), use_container_width=True)
    else:
        st.info("Upload a data file and select a sheet to see analytics.")

def errorlogs_page():
    st.title("Error Logs")
    st.write("View and manage system error logs.")
    # Use error logs from session state if available
    error_logs = st.session_state.get('error_logs', [])
    error_data = {
        "Error ID": [e['Error ID'] for e in error_logs] if error_logs else ["ERR-2024-001", "ERR-2024-002"],
        "Type": [e['Type'] for e in error_logs] if error_logs else ["High", "Medium"],
        "Message": [e['Message'] for e in error_logs] if error_logs else ["Missing supervisor name in row 5 of well_data_batch_12.xlsx", "Invalid zip code format in customer_update_jan15.xlsx"],
        "Date": [e['Date'] for e in error_logs] if error_logs else ["2024-01-15", "2024-01-14"],
        "Status": [e['Status'] for e in error_logs] if error_logs else ["Open", "Closed"]
    }
    df_errors = pd.DataFrame(error_data)
    st.markdown(f"<div style='background:{CARD_COLOR};border-radius:10px;padding:1rem 1rem 1rem 1rem;border:1px solid {PRIMARY_COLOR};margin-top:1rem;'><h4 style='color:{ACCENT_COLOR};margin-bottom:0.5rem;'>Error Logs</h4>", unsafe_allow_html=True)
    st.dataframe(df_errors, use_container_width=True)
    st.markdown("<hr>")
    st.markdown(f"<h4 style='color:{ACCENT_COLOR};'>Add New Error</h4>", unsafe_allow_html=True)
    with st.form("add_error_form"):
        new_error_id = st.text_input("Error ID", key="add_error_id")
        new_error_type = st.selectbox("Type", ["High", "Medium", "Low"], key="add_error_type")
        new_error_message = st.text_area("Message", key="add_error_message")
        new_error_date = st.date_input("Date", key="add_error_date")
        new_error_status = st.selectbox("Status", ["Open", "Closed"], key="add_error_status")
        submitted = st.form_submit_button("Add Error")
        if submitted:
            if 'error_logs' not in st.session_state:
                st.session_state['error_logs'] = []
            st.session_state['error_logs'].append({
                'Error ID': new_error_id,
                'Type': new_error_type,
                'Message': new_error_message,
                'Date': str(new_error_date),
                'Status': new_error_status
            })
            st.success(f"Error '{new_error_id}' added (not saved in prototype)")

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
    st.markdown("<hr>")
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