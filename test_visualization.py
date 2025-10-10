import pandas as pd
import matplotlib.pyplot as plt
import collections
from datetime import datetime
import os

def create_sample_data():
    """Create sample job data for testing"""
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

def process_and_save_data(data: list[dict]):
    """Converts data to DataFrame, removes duplicates, and saves to CSV."""
    if not data:
        print("No data to save.")
        return None

    df = pd.DataFrame(data)
    print(f"Raw listings collected: {len(df)}")
    
    # Remove duplicates based on Job Title, Company, and Link
    df_cleaned = df.drop_duplicates(subset=['Job Title', 'Company', 'Link'], keep='first')
    
    # Save the cleaned data with a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f'linkedin_jobs_test_{timestamp}.csv'
    df_cleaned.to_csv(final_filename, index=False)
    
    print(f"Duplicates removed: {len(df) - len(df_cleaned)}")
    print(f"✅ Final data saved to {final_filename} with {len(df_cleaned)} unique listings.")
    
    return df_cleaned, final_filename

def create_visualization(df: pd.DataFrame, filename: str = None):
    """Creates a bar chart of job frequency by company and saves it as PNG."""
    if df.empty:
        print("No data to visualize.")
        return None
        
    # Count jobs by company
    company_counts = collections.Counter(df['Company'])
    
    # Get top 10 companies
    top_companies = dict(company_counts.most_common(10))
    
    if not top_companies:
        print("No company data to visualize.")
        return None
    
    # Create bar chart
    plt.figure(figsize=(12, 8))
    companies = list(top_companies.keys())
    counts = list(top_companies.values())
    
    bars = plt.bar(range(len(companies)), counts, color='skyblue')
    plt.xlabel('Company')
    plt.ylabel('Number of Job Postings')
    plt.title('Top 10 Companies by Job Postings')
    plt.xticks(range(len(companies)), companies, rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save with timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if filename:
        # Use the same timestamp as the CSV file for consistency
        png_filename = filename.replace('.csv', '_graph.png')
    else:
        png_filename = f'company_job_frequency_graph_{timestamp}.png'
        
    plt.savefig(png_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Visualization saved to {png_filename}")
    return png_filename

def main():
    """Test the data processing and visualization functions"""
    print("🔍 Testing data processing and visualization functions")
    
    # Create sample data
    sample_data = create_sample_data()
    print(f"Created sample data with {len(sample_data)} entries")
    
    # Process and save data
    df_cleaned, csv_filename = process_and_save_data(sample_data)
    
    # Create visualization
    if df_cleaned is not None and not df_cleaned.empty:
        png_filename = create_visualization(df_cleaned, csv_filename)
        print(f"📊 Data visualization completed: {png_filename}")
        
        # Show the contents of the CSV file
        print("\n📄 CSV File Contents:")
        df = pd.read_csv(csv_filename)
        print(df.to_string(index=False))
        
        # Show the generated PNG file exists
        if os.path.exists(png_filename):
            print(f"\n✅ Visualization file created: {png_filename}")
        else:
            print(f"\n❌ Visualization file not found: {png_filename}")
    else:
        print("❌ No data to visualize")

if __name__ == "__main__":
    main()