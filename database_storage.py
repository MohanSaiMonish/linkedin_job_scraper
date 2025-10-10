"""
Database storage version of the LinkedIn job scraper data processing
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

def create_database(db_name="linkedin_jobs.db"):
    """Create SQLite database and jobs table"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            company TEXT,
            location TEXT,
            post_date TEXT,
            link TEXT,
            search_keywords TEXT,
            search_location TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(job_title, company, link)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database {db_name} created/initialized")

def save_to_database(data: list[dict], db_name="linkedin_jobs.db"):
    """Save job data to SQLite database"""
    if not data:
        print("No data to save to database")
        return 0
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Insert data, ignoring duplicates
    inserted_count = 0
    for job in data:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO jobs 
                (job_title, company, location, post_date, link, search_keywords, search_location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                job.get('Job Title', ''),
                job.get('Company', ''),
                job.get('Location', ''),
                job.get('Post Date', ''),
                job.get('Link', ''),
                job.get('Search Keywords', ''),
                job.get('Search Location', '')
            ))
            if cursor.rowcount > 0:
                inserted_count += 1
        except Exception as e:
            print(f"Error inserting job: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"✅ Saved {inserted_count} new jobs to database (duplicates ignored)")
    return inserted_count

def get_jobs_from_database(db_name="linkedin_jobs.db", limit=100):
    """Retrieve jobs from database"""
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query("SELECT * FROM jobs ORDER BY scraped_at DESC LIMIT ?", conn, params=(limit,))
    conn.close()
    return df

def export_database_to_csv(db_name="linkedin_jobs.db", csv_filename=None):
    """Export database to CSV file"""
    if csv_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"linkedin_jobs_database_{timestamp}.csv"
    
    df = get_jobs_from_database(db_name)
    df.to_csv(csv_filename, index=False)
    print(f"✅ Database exported to {csv_filename}")
    return csv_filename

def get_company_stats(db_name="linkedin_jobs.db"):
    """Get company job statistics"""
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query('''
        SELECT company, COUNT(*) as job_count 
        FROM jobs 
        GROUP BY company 
        ORDER BY job_count DESC 
        LIMIT 10
    ''', conn)
    conn.close()
    return df

def main():
    """Test database functionality"""
    print("🔍 Testing database storage functionality")
    
    # Create database
    create_database()
    
    # Sample data
    sample_data = [
        {'Job Title': 'Data Analyst', 'Company': 'Tech Solutions Inc', 'Location': 'New York, NY', 'Post Date': '2023-10-15', 'Link': 'https://linkedin.com/jobs/view/12345', 'Search Keywords': 'Data Analyst', 'Search Location': 'New York City Metro Area'},
        {'Job Title': 'Senior Data Analyst', 'Company': 'Finance Corp', 'Location': 'Boston, MA', 'Post Date': '2023-10-14', 'Link': 'https://linkedin.com/jobs/view/12346', 'Search Keywords': 'Data Analyst', 'Search Location': 'New York City Metro Area'},
        {'Job Title': 'Data Scientist', 'Company': 'Tech Solutions Inc', 'Location': 'San Francisco, CA', 'Post Date': '2023-10-13', 'Link': 'https://linkedin.com/jobs/view/12347', 'Search Keywords': 'Data Analyst', 'Search Location': 'New York City Metro Area'},
    ]
    
    # Save to database
    save_to_database(sample_data)
    
    # Retrieve and display data
    df = get_jobs_from_database()
    print("\n📄 Database Contents (latest 10 entries):")
    print(df.to_string(index=False))
    
    # Show company statistics
    company_stats = get_company_stats()
    print("\n📊 Top Companies by Job Count:")
    print(company_stats.to_string(index=False))
    
    # Export to CSV
    csv_file = export_database_to_csv()
    print(f"\n📁 Exported database to: {csv_file}")

if __name__ == "__main__":
    main()