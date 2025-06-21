import streamlit as st
import pandas as pd
from app.utils import process_leads # importing the function to process leads
import os

# --- Page Configuration ---
# `set_page_config` must be the first Streamlit command to run.
st.set_page_config(
    page_title="Lead Scorer Tool",
    page_icon="🐐",
    layout="wide" # Using wide layout for data tables
)

# --- Function to Convert to CSV (for Download Button) ---
@st.cache_data # Cache data to avoid re-conversion on every render
def convert_df_to_csv(df):
    """Convert DataFrame to CSV (UTF-8) format for download."""
    return df.to_csv(index=False).encode('utf-8')

# --- App Title and Description ---
st.title("Lead Prioritization Tool")
st.markdown("""
This application helps prioritize leads from **SaaSquatchLeads.com** by providing **scores** and **data quality flags**.
Upload your CSV file to get started, or use the provided demo data.
""")

# --- Sidebar: Control & Filter ---
st.sidebar.header("⚙️ Control & Filter")

# File Uploader in Sidebar
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV file here",
    type=['csv']
)

# --- Main Logic: Load and Process Data ---
df_raw = None
if uploaded_file is not None:
    # If user uploads a file, use that file
    try:
        df_raw = pd.read_csv(uploaded_file)
        st.sidebar.success("File successfully uploaded!")
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")
else:
    # If no file is uploaded, use demo data
    demo_file_path = os.path.join('data', 'saasquatch_leads_dummy.csv')
    if os.path.exists(demo_file_path):
        df_raw = pd.read_csv(demo_file_path)
        st.sidebar.info("Displaying demo data. Upload your file above.")
    else:
        st.error("Demo data file (saasquatch_leads_dummy.csv) not found in 'data' folder.")


# Only proceed if DataFrame is successfully loaded
if df_raw is not None:
    # Process DataFrame using functions from utils.py
    df_processed = process_leads(df_raw)

    # --- Add Filters in Sidebar ---

    # 1. Filter by Score Range
    min_score, max_score = int(df_processed['Score'].min()), int(df_processed['Score'].max())
    score_range = st.sidebar.slider(
        "Filter by Score:",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score) # Defaultnya menampilkan semua skor
    )

    # 2. Filter by Industry (Multi-select)
    all_industries = sorted(df_processed['Industry'].dropna().unique())
    selected_industries = st.sidebar.multiselect(
        "Filter by Industry:",
        options=all_industries,
        default=[] # Defaultnya tidak ada yang dipilih (tampilkan semua)
    )

    # 3. Filter by Flags (Text search)
    # This allows users to search for leads with specific data issues
    flag_query = st.sidebar.text_input(
        "Search leads with specific Flag:",
        placeholder="e.g., Missing Email"
    )

    # --- Apply Filters to DataFrame ---
    df_filtered = df_processed[
        (df_processed['Score'] >= score_range[0]) & (df_processed['Score'] <= score_range[1])
    ]

    if selected_industries: # If user selects industries
        df_filtered = df_filtered[df_filtered['Industry'].isin(selected_industries)]

    if flag_query: # If user types something in flag search
        df_filtered = df_filtered[df_filtered['Flags'].str.contains(flag_query, case=False, na=False)]

    # --- Main Display: Analysis Results ---
    st.header("Analysis Results & Lead Prioritization")

    # Display summary metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Leads Processed", len(df_processed))
    col2.metric("Leads Matching Filter", len(df_filtered), f"{len(df_filtered) - len(df_processed)}")

    # Display filtered data table
    st.dataframe(df_filtered, use_container_width=True, height=500)

    # --- Download Button ---
    csv_data = convert_df_to_csv(df_filtered)
    
    st.download_button(
       label="Download Filtered Results (CSV)",
       data=csv_data,
       file_name=f"scored_leads_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
       mime='text/csv',
    )
else:
    st.info("Waiting for CSV file to be processed...")