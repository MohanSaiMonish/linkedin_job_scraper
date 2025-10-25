import pandas as pd
import matplotlib.pyplot as plt
import csv
from collections import Counter

def create_demo_data():
    """Create demo job data for different roles and locations"""
    demo_jobs = [
        # Software Engineer jobs in San Francisco
        {'Job Title': 'Senior Software Engineer', 'Company': 'Google', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-15'},
        {'Job Title': 'Full Stack Developer', 'Company': 'Meta', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-14'},
        {'Job Title': 'Software Engineer', 'Company': 'Apple', 'Location': 'Cupertino, CA', 'Date Posted': '2024-01-13'},
        {'Job Title': 'Backend Engineer', 'Company': 'Netflix', 'Location': 'Los Gatos, CA', 'Date Posted': '2024-01-12'},
        {'Job Title': 'Frontend Developer', 'Company': 'Uber', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-11'},
        {'Job Title': 'Software Engineer', 'Company': 'Salesforce', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-10'},
        {'Job Title': 'DevOps Engineer', 'Company': 'Twitter', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-09'},
        {'Job Title': 'Machine Learning Engineer', 'Company': 'Tesla', 'Location': 'Palo Alto, CA', 'Date Posted': '2024-01-08'},
        {'Job Title': 'Software Engineer', 'Company': 'Airbnb', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-07'},
        {'Job Title': 'Senior Developer', 'Company': 'LinkedIn', 'Location': 'Sunnyvale, CA', 'Date Posted': '2024-01-06'},
        
        # Data Analyst jobs in New York
        {'Job Title': 'Senior Data Analyst', 'Company': 'Goldman Sachs', 'Location': 'New York, NY', 'Date Posted': '2024-01-15'},
        {'Job Title': 'Business Intelligence Analyst', 'Company': 'JPMorgan Chase', 'Location': 'New York, NY', 'Date Posted': '2024-01-14'},
        {'Job Title': 'Data Analyst', 'Company': 'Morgan Stanley', 'Location': 'New York, NY', 'Date Posted': '2024-01-13'},
        {'Job Title': 'Financial Data Analyst', 'Company': 'BlackRock', 'Location': 'New York, NY', 'Date Posted': '2024-01-12'},
        {'Job Title': 'Marketing Data Analyst', 'Company': 'American Express', 'Location': 'New York, NY', 'Date Posted': '2024-01-11'},
        {'Job Title': 'Data Analyst', 'Company': 'Citigroup', 'Location': 'New York, NY', 'Date Posted': '2024-01-10'},
        {'Job Title': 'Business Analyst', 'Company': 'Bank of America', 'Location': 'New York, NY', 'Date Posted': '2024-01-09'},
        {'Job Title': 'Data Scientist', 'Company': 'Bloomberg', 'Location': 'New York, NY', 'Date Posted': '2024-01-08'},
        {'Job Title': 'Analytics Manager', 'Company': 'Visa', 'Location': 'New York, NY', 'Date Posted': '2024-01-07'},
        {'Job Title': 'Data Analyst', 'Company': 'Mastercard', 'Location': 'New York, NY', 'Date Posted': '2024-01-06'},
        
        # Product Manager jobs in Seattle
        {'Job Title': 'Senior Product Manager', 'Company': 'Amazon', 'Location': 'Seattle, WA', 'Date Posted': '2024-01-15'},
        {'Job Title': 'Product Manager', 'Company': 'Microsoft', 'Location': 'Redmond, WA', 'Date Posted': '2024-01-14'},
        {'Job Title': 'Technical Product Manager', 'Company': 'Starbucks', 'Location': 'Seattle, WA', 'Date Posted': '2024-01-13'},
        {'Job Title': 'Product Owner', 'Company': 'Boeing', 'Location': 'Seattle, WA', 'Date Posted': '2024-01-12'},
        {'Job Title': 'Product Manager', 'Company': 'Expedia', 'Location': 'Seattle, WA', 'Date Posted': '2024-01-11'},
    ]
    return demo_jobs

def save_to_csv(jobs_data, filename="linkedin_jobs_demo.csv"):
    """Save job data to CSV file"""
    if not jobs_data:
        print("No job data to save.")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Job Title', 'Company', 'Location', 'Date Posted']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs_data)
    
    print(f"✅ Saved {len(jobs_data)} jobs to {filename}")

def create_visualization(jobs_data, keywords, location):
    """Create job/company visualization"""
    if not jobs_data:
        print("No data to visualize.")
        return
    
    df = pd.DataFrame(jobs_data)
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'LinkedIn Jobs Analysis: {keywords} in {location}', fontsize=16)
    
    # 1. Top Companies by Job Count
    company_counts = df['Company'].value_counts().head(10)
    company_counts.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Top 10 Companies by Job Count')
    ax1.set_xlabel('Company')
    ax1.set_ylabel('Number of Jobs')
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Job Distribution by Location
    location_counts = df['Location'].value_counts().head(10)
    location_counts.plot(kind='bar', ax=ax2, color='lightgreen')
    ax2.set_title('Job Distribution by Location')
    ax2.set_xlabel('Location')
    ax2.set_ylabel('Number of Jobs')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Job Titles Word Cloud (simplified as bar chart)
    title_words = ' '.join(df['Job Title']).lower().split()
    word_counts = Counter([word for word in title_words if len(word) > 3])
    top_words = dict(word_counts.most_common(10))
    
    words = list(top_words.keys())
    counts = list(top_words.values())
    ax3.bar(words, counts, color='orange')
    ax3.set_title('Most Common Words in Job Titles')
    ax3.set_xlabel('Words')
    ax3.set_ylabel('Frequency')
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. Jobs by Date (if available)
    if 'Date Posted' in df.columns:
        df['Date Posted'] = pd.to_datetime(df['Date Posted'], errors='coerce')
        daily_jobs = df.groupby(df['Date Posted'].dt.date).size()
        daily_jobs.plot(kind='line', ax=ax4, marker='o', color='red')
        ax4.set_title('Jobs Posted Over Time')
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Number of Jobs')
        ax4.tick_params(axis='x', rotation=45)
    else:
        ax4.text(0.5, 0.5, 'Date data not available', ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title('Date Analysis Not Available')
    
    plt.tight_layout()
    plt.savefig('linkedin_jobs_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Visualization saved as 'linkedin_jobs_analysis.png'")
    plt.show()

def filter_jobs_by_role(jobs_data, role_keywords, location_keywords):
    """Filter jobs by role and location keywords"""
    filtered_jobs = []
    for job in jobs_data:
        title_match = any(keyword.lower() in job['Job Title'].lower() for keyword in role_keywords)
        location_match = any(keyword.lower() in job['Location'].lower() for keyword in location_keywords)
        
        if title_match and location_match:
            filtered_jobs.append(job)
    
    return filtered_jobs

if __name__ == "__main__":
    # Configuration - Change these values
    JOB_KEYWORDS = "Software Engineer"  # Change role here
    JOB_LOCATION = "San Francisco"  # Change location here
    
    print(f"🔍 Analyzing jobs for: {JOB_KEYWORDS} in {JOB_LOCATION}")
    
    # Create demo data
    all_jobs = create_demo_data()
    
    # Filter jobs by role and location
    role_keywords = JOB_KEYWORDS.split()
    location_keywords = JOB_LOCATION.split()
    filtered_jobs = filter_jobs_by_role(all_jobs, role_keywords, location_keywords)
    
    if filtered_jobs:
        # Save to CSV
        save_to_csv(filtered_jobs, f"linkedin_jobs_{JOB_KEYWORDS.replace(' ', '_').lower()}.csv")
        
        # Create visualization
        create_visualization(filtered_jobs, JOB_KEYWORDS, JOB_LOCATION)
        
        print(f"\n📊 Analysis Complete!")
        print(f"✅ Found {len(filtered_jobs)} jobs matching criteria")
        print(f"✅ Saved to CSV file")
        print(f"✅ Created visualization")
        
        # Show sample data
        print(f"\n📋 Sample Jobs:")
        for i, job in enumerate(filtered_jobs[:5]):
            print(f"{i+1}. {job['Job Title']} at {job['Company']} ({job['Location']})")
    else:
        print("❌ No jobs found matching criteria")
        print("Available roles: Software Engineer, Data Analyst, Product Manager")
        print("Available locations: San Francisco, New York, Seattle")
