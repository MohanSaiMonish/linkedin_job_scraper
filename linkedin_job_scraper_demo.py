import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import time

def create_sample_data():
    """Create sample job data for demonstration"""
    sample_data = [
        {'Job Title': 'Data Analyst', 'Company': 'Tech Solutions Inc', 'Location': 'New York, NY', 'Post Date': '2023-10-15', 'Link': 'https://linkedin.com/jobs/view/12345'},
        {'Job Title': 'Senior Data Analyst', 'Company': 'Finance Corp', 'Location': 'Boston, MA', 'Post Date': '2023-10-14', 'Link': 'https://linkedin.com/jobs/view/12346'},
        {'Job Title': 'Data Scientist', 'Company': 'Tech Solutions Inc', 'Location': 'San Francisco, CA', 'Post Date': '2023-10-13', 'Link': 'https://linkedin.com/jobs/view/12347'},
        {'Job Title': 'Business Analyst', 'Company': 'Retail Giant', 'Location': 'Chicago, IL', 'Post Date': '2023-10-12', 'Link': 'https://linkedin.com/jobs/view/12348'},
        {'Job Title': 'Data Engineer', 'Company': 'Tech Solutions Inc', 'Location': 'Seattle, WA', 'Post Date': '2023-10-11', 'Link': 'https://linkedin.com/jobs/view/12349'},
        {'Job Title': 'Product Analyst', 'Company': 'StartupXYZ', 'Location': 'Austin, TX', 'Post Date': '2023-10-10', 'Link': 'https://linkedin.com/jobs/view/12350'},
        {'Job Title': 'Marketing Analyst', 'Company': 'Marketing Pro', 'Location': 'New York, NY', 'Post Date': '2023-10-09', 'Link': 'https://linkedin.com/jobs/view/12351'},
        {'Job Title': 'Financial Analyst', 'Company': 'Finance Corp', 'Location': 'Boston, MA', 'Post Date': '2023-10-08', 'Link': 'https://linkedin.com/jobs/view/12352'},
        {'Job Title': 'Data Analyst', 'Company': 'HealthPlus', 'Location': 'Boston, MA', 'Post Date': '2023-10-07', 'Link': 'https://linkedin.com/jobs/view/12353'},
        {'Job Title': 'Research Analyst', 'Company': 'Research Institute', 'Location': 'Washington, DC', 'Post Date': '2023-10-06', 'Link': 'https://linkedin.com/jobs/view/12354'},
        {'Job Title': 'Data Analyst', 'Company': 'Tech Solutions Inc', 'Location': 'New York, NY', 'Post Date': '2023-10-05', 'Link': 'https://linkedin.com/jobs/view/12355'},  # Duplicate for testing
    ]
    return sample_data

def save_to_csv(data, filename='linkedin_jobs_demo.csv'):
    """Save job data to CSV file"""
    if not data:
        print("No data to save")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    print(f"📊 Raw data contains {len(df)} listings")
    
    # Remove duplicates based on job title and company
    df_cleaned = df.drop_duplicates(subset=['Job Title', 'Company'], keep='first')
    print(f"🧹 Removed {len(df) - len(df_cleaned)} duplicate listings")
    
    # Save to CSV
    df_cleaned.to_csv(filename, index=False)
    print(f"✅ Saved {len(df_cleaned)} unique jobs to {filename}")
    return df_cleaned

def visualize_job_frequency(df, filename='company_job_frequency_demo.png'):
    """Create a bar chart of job frequency by company"""
    if df.empty:
        print("No data to visualize")
        return
    
    # Count jobs by company
    company_counts = Counter(df['Company'])
    
    # Get top 10 companies
    top_companies = dict(company_counts.most_common(10))
    
    # Create bar chart
    plt.figure(figsize=(12, 6))
    companies = list(top_companies.keys())
    counts = list(top_companies.values())
    
    bars = plt.bar(companies, counts, color='skyblue')
    plt.xlabel('Company')
    plt.ylabel('Number of Job Postings')
    plt.title('Top 10 Companies by Job Postings')
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Saved visualization to {filename}")
    return filename

def main():
    """Demo main function"""
    print("🚀 LinkedIn Job Scraper - Demo Mode")
    print("=" * 50)
    
    # Simulate scraping process
    print("🔍 Searching for jobs...")
    time.sleep(1)
    print("🖱️  Scrolling through job listings...")
    time.sleep(1)
    print("📊 Extracting job data...")
    time.sleep(1)
    
    # Create sample data
    jobs_data = create_sample_data()
    print(f"✅ Extracted {len(jobs_data)} job listings")
    
    # Save to CSV
    print("\n💾 Saving to CSV...")
    df = save_to_csv(jobs_data)
    
    # Create visualization
    print("\n📈 Creating visualization...")
    viz_file = visualize_job_frequency(df)
    
    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("\n📁 Generated files:")
    print(f"   - linkedin_jobs_demo.csv")
    print(f"   - company_job_frequency_demo.png")
    print("\n💡 In real usage, the script would:")
    print("   1. Log into LinkedIn with your credentials")
    print("   2. Search for jobs based on your keywords")
    print("   3. Automatically scroll to load more listings")
    print("   4. Extract job details using web scraping")
    print("   5. Save unique listings to a CSV file")
    print("   6. Create a visualization of company job frequencies")

if __name__ == "__main__":
    main()