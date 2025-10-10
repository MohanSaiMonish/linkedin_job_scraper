# LinkedIn Job Scraper

A Python script to automatically scrape job listings from LinkedIn, save them to a CSV file, and visualize job frequency by company. Includes an interactive dashboard for data exploration.

## Features

- Automates LinkedIn job search
- Extracts job titles, companies, locations, and post dates
- Removes duplicate listings
- Saves data to CSV
- Creates visualization of job frequency by company
- Interactive dashboard for data exploration

## Requirements

- Python 3.7+
- Google Chrome browser
- LinkedIn account

## Installation

1. Clone this repository or download the files
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python linkedin_job_scraper.py
   ```

2. Enter your LinkedIn credentials when prompted
3. Enter job search keywords and location when prompted
4. The script will:
   - Log into LinkedIn
   - Search for jobs
   - Scroll to load more listings
   - Extract job data
   - Save to a CSV file
   - Create a visualization

## Interactive Dashboards

After running the scraper and generating a CSV file, you can explore the data using the interactive Streamlit dashboard, or generate static visualizations:

### Streamlit Dashboard

1. Install Streamlit (if not already installed):
   ```
   pip install streamlit
   ```

2. Run the Streamlit dashboard:
   ```
   streamlit run streamlit_dashboard.py
   ```

3. The dashboard will open automatically in your browser, or you can access it at `http://localhost:8501`

The Streamlit dashboard includes:
- File uploader for CSV data
- Data preview
- Bar charts for company and location frequency
- Pie chart for popular job titles

### Simple Static Dashboard

For a lightweight, no-dependency solution, you can generate static visualizations:

1. Run the simple dashboard script:
   ```
   python simple_dashboard.py
   ```

2. View the generated visualizations in the `figures` directory:
   - `company_frequency.png` - Bar chart of top companies
   - `location_frequency.png` - Bar chart of top locations
   - `job_titles.png` - Pie chart of popular job titles

This approach uses only standard libraries and pandas, avoiding any complex dependencies or web frameworks.

## Output

- `linkedin_jobs.csv` - Contains job listings with columns:
  - Job Title
  - Company
  - Location
  - Post Date
  - Link

- `company_job_frequency.png` - Bar chart showing top companies by job count

## Note

This script is for educational purposes only. Be sure to comply with LinkedIn's Terms of Service and use the script responsibly.
