import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# CSS to keep buttons horizontal
st.markdown("""
    <style>
        .horizontal-buttons > div {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .horizontal-buttons button {
            margin: 0 !important;
            white-space: nowrap;
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Weight Tracker")

# ----- Google Sheets connection -----
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)

SHEET_NAME = "weight_tracker_data"
sheet = client.open(SHEET_NAME).sheet1

# ----- Load and prepare data -----
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not data or "Date" not in data[0]:
    df = pd.DataFrame(columns=["Date", "Weight"])

st.title("🏋️ Weight Tracker")

# ----- Input weight -----
today = datetime.date.today().isoformat()
weight_input = st.number_input("Enter today's weight (kg):", min_value=0.0, step=0.1)

if st.button("Add today's weight"):
    df = df[df["Date"] != today]
    df.loc[len(df.index)] = [today, weight_input]
    sheet.clear()
    sheet.append_row(["Date", "Weight"])
    for row in df.values.tolist():
        sheet.append_row(row)
    st.success("Weight saved to Google Sheets!")
    st.rerun()

# ----- Session state toggles -----
if "show_full_history" not in st.session_state:
    st.session_state.show_full_history = False
if "show_full_chart" not in st.session_state:
    st.session_state.show_full_chart = True

# ----- Handle row deletion -----
if "delete_row_confirmed" in st.session_state:
    delete_index = st.session_state["delete_row_confirmed"]
    df = df.drop(index=delete_index).reset_index(drop=True)
    del st.session_state["delete_row_confirmed"]
    sheet.clear()
    sheet.append_row(["Date", "Weight"])
    for row in df.values.tolist():
        sheet.append_row(row)
    st.success("Entry deleted!")
    st.rerun()

# ----- Sort dataframe by date -----
df_sorted = df.sort_values("Date").reset_index(drop=True)

# ----- Graph Section -----
st.subheader("📈 Progress Over Time")
chart_cols = st.columns([0.5, 0.5], gap="small")
with chart_cols[0]:
    if st.button("Last 7 Days Chart", key="chart_last7"):
        st.session_state.show_full_chart = False
with chart_cols[1]:
    if st.button("Full Chart", key="chart_all"):
        st.session_state.show_full_chart = True

if not df.empty:
    df_sorted["Date"] = pd.to_datetime(df_sorted["Date"])
    df_sorted.set_index("Date", inplace=True)
    chart_df = df_sorted.tail(7) if not st.session_state.show_full_chart else df_sorted
    st.line_chart(chart_df["Weight"])
    df_sorted.reset_index(inplace=True)
    df_sorted["Date"] = df_sorted["Date"].dt.strftime("%Y-%m-%d")  # ⬅️ Remove time-of-day
else:
    st.info("No data to show yet.")

# ----- Weight History Table -----
st.subheader("📅 Weight History")
history_cols = st.columns([0.5, 0.5], gap="small")
with history_cols[0]:
    if st.button("Last 7 Days", key="history_last7"):
        st.session_state.show_full_history = False
with history_cols[1]:
    if st.button("Entire List", key="history_all"):
        st.session_state.show_full_history = True

display_df = df_sorted.tail(7).reset_index(drop=True) if not st.session_state.show_full_history else df_sorted.reset_index(drop=True)

# Determine pagination for AgGrid
if st.session_state.show_full_history:
    pagination = False
    pagination_page_size = max(len(display_df), 20)
else:
    pagination = False
    pagination_page_size = len(display_df)

gb = GridOptionsBuilder.from_dataframe(display_df)
gb.configure_selection(selection_mode="single", use_checkbox=False)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=pagination_page_size)
gb.configure_column("Date", width=120)
gb.configure_column("Weight", width=100)
grid_options = gb.build()

grid_response = AgGrid(
    display_df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    allow_unsafe_jscode=True,
    height=80 + pagination_page_size * 28,  # 28 px per row approx + header
    fit_columns_on_grid_load=True,
)


# ----- Deletion logic -----
selected = grid_response.get("selected_rows", [])

if selected and len(selected) > 0:
    selected_row = selected[0]
    selected_date = selected_row["Date"]
    selected_index = display_df.index[display_df["Date"] == selected_date].tolist()
    if selected_index:
        selected_idx = selected_index[0]
        st.warning(
            f"Are you sure you want to delete the entry from **{display_df.loc[selected_idx, 'Date']} ({display_df.loc[selected_idx, 'Weight']} kg)**?"
        )
        col_confirm, col_cancel = st.columns([0.5, 0.5], gap="small")
        with col_confirm:
            if st.button("✅ Yes, delete it", key="confirm_delete"):
                # Convert to datetime for matching in df_sorted
                actual_idx = df_sorted.index[df_sorted["Date"] == selected_date].tolist()
                if actual_idx:
                    st.session_state["delete_row_confirmed"] = actual_idx[0]
                    st.rerun()
        with col_cancel:
            if st.button("❌ Cancel", key="cancel_delete"):
                st.rerun()
