import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import glob
from collections import Counter

st.set_page_config(page_title="LinkedIn Jobs Dashboard", page_icon="💼", layout="wide")

st.title("💼 LinkedIn Job Scraper Dashboard")
st.markdown("Explore and visualize LinkedIn job data")

csv_files = glob.glob("*.csv")
csv_files = [f for f in csv_files if f.startswith("linkedin_jobs") or f.startswith("comprehensive_test")]

if csv_files:
    selected_file = st.sidebar.selectbox("Select CSV file", csv_files, index=0)
    
    if st.sidebar.button("Reload Data"):
        st.cache_data.clear()
        st.rerun()
else:
    st.sidebar.info("No CSV files found. Upload a file below or run the scraper first.")
    selected_file = None

uploaded_file = st.sidebar.file_uploader("Or upload a CSV file", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded {len(df)} jobs from uploaded file")
elif selected_file:
    df = pd.read_csv(selected_file)
    st.sidebar.success(f"Loaded {len(df)} jobs from {selected_file}")
else:
    st.info("👆 Please select or upload a CSV file to get started")
    st.stop()

st.subheader("📊 Data Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jobs", len(df))
with col2:
    st.metric("Unique Companies", df['Company'].nunique())
with col3:
    st.metric("Unique Locations", df['Location'].nunique())
with col4:
    st.metric("Unique Job Titles", df['Job Title'].nunique())

st.subheader("🔍 Filter Data")
col1, col2 = st.columns(2)

with col1:
    companies = ['All'] + sorted(df['Company'].unique().tolist())
    selected_company = st.selectbox("Filter by Company", companies)

with col2:
    locations = ['All'] + sorted(df['Location'].unique().tolist())
    selected_location = st.selectbox("Filter by Location", locations)

filtered_df = df.copy()
if selected_company != 'All':
    filtered_df = filtered_df[filtered_df['Company'] == selected_company]
if selected_location != 'All':
    filtered_df = filtered_df[filtered_df['Location'] == selected_location]

st.subheader("📋 Job Listings")
st.dataframe(
    filtered_df[['Job Title', 'Company', 'Location', 'Post Date']],
    use_container_width=True,
    height=400
)

if 'Link' in filtered_df.columns:
    st.markdown("### 🔗 Quick Links")
    for idx, row in filtered_df.head(10).iterrows():
        if pd.notna(row.get('Link')):
            st.markdown(f"- [{row['Job Title']} at {row['Company']}]({row['Link']})")

st.subheader("📈 Visualizations")

tab1, tab2, tab3 = st.tabs(["Company Analysis", "Location Analysis", "Job Title Analysis"])

with tab1:
    st.markdown("#### Top Companies by Job Count")
    company_counts = df['Company'].value_counts().head(15)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    company_counts.plot(kind='barh', ax=ax, color='#0077B5')
    ax.set_xlabel('Number of Jobs')
    ax.set_ylabel('Company')
    ax.set_title('Top 15 Companies by Job Count')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with tab2:
    st.markdown("#### Top Locations by Job Count")
    location_counts = df['Location'].value_counts().head(15)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    location_counts.plot(kind='barh', ax=ax, color='#00A0DC')
    ax.set_xlabel('Number of Jobs')
    ax.set_ylabel('Location')
    ax.set_title('Top 15 Locations by Job Count')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with tab3:
    st.markdown("#### Top Job Titles")
    title_counts = df['Job Title'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.Set3(range(len(title_counts)))
    wedges, texts, autotexts = ax.pie(
        title_counts.values, 
        labels=title_counts.index, 
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    ax.set_title('Top 10 Job Titles Distribution')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Statistics")
st.sidebar.write(f"**Dataset:** {selected_file if selected_file else 'Uploaded file'}")
st.sidebar.write(f"**Total rows:** {len(df)}")
st.sidebar.write(f"**Filtered rows:** {len(filtered_df)}")

if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

if st.sidebar.button("Download Filtered Data"):
    csv = filtered_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"filtered_jobs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
