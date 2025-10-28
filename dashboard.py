import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup
st.set_page_config(page_title="LinkedIn Job Dashboard", layout="wide")

# Title
st.title("💼 LinkedIn Job Insights Dashboard")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("jobs_data.csv")

df = load_data()

# Basic stats
st.subheader("📄 Data Overview")
st.write(df.head())

st.write("Total Jobs Found:", len(df))
st.write("Unique Companies:", df['Company'].nunique())

# Remove duplicates
df.drop_duplicates(inplace=True)

# Filters
st.sidebar.header("🔍 Filter Options")
selected_company = st.sidebar.selectbox("Select Company", ["All"] + sorted(df['Company'].unique().tolist()))
selected_keyword = st.sidebar.text_input("Search by Keyword")

# Apply filters
filtered_df = df.copy()
if selected_company != "All":
    filtered_df = filtered_df[filtered_df['Company'] == selected_company]
if selected_keyword:
    filtered_df = filtered_df[filtered_df['Title'].str.contains(selected_keyword, case=False, na=False)]

st.subheader("📋 Filtered Job Listings")
st.dataframe(filtered_df)

# Visualization 1: Jobs per Company
st.subheader("🏢 Job Frequency by Company")
company_counts = df['Company'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=company_counts.values, y=company_counts.index, ax=ax)
ax.set_xlabel("Number of Job Posts")
ax.set_ylabel("Company")
st.pyplot(fig)

# Visualization 2: Jobs Over Time
if 'Post Date' in df.columns:
    st.subheader("⏰ Job Posts Over Time")
    df['Post Date'] = pd.to_datetime(df['Post Date'], errors='coerce')
    date_counts = df['Post Date'].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    ax2.plot(date_counts.index, date_counts.values, marker='o')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Jobs Posted")
    st.pyplot(fig2)

st.success("✅ Dashboard loaded successfully!")