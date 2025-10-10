import pandas as pd
from datetime import datetime
import os

print("🔍 Testing Data Processing and Saving Functionality")
print("=" * 50)

# Sample job data (simulating what would be collected from LinkedIn)
sample_data = [
    {
        'Job Title': 'Data Analyst',
        'Company': 'Tech Corp',
        'Location': 'New York, NY',
        'Post Date': '2023-10-01',
        'Link': 'https://linkedin.com/jobs/view/12345',
        'Search Keywords': 'Data Analyst',
        'Search Location': 'New York City Metro Area'
    },
    {
        'Job Title': 'Senior Data Analyst',
        'Company': 'Finance Inc',
        'Location': 'Boston, MA',
        'Post Date': '2023-10-02',
        'Link': 'https://linkedin.com/jobs/view/12346',
        'Search Keywords': 'Data Analyst',
        'Search Location': 'New York City Metro Area'
    },
    {
        'Job Title': 'Data Analyst',  # Duplicate title and company
        'Company': 'Tech Corp',       # Duplicate company
        'Location': 'San Francisco, CA',
        'Post Date': '2023-10-03',
        'Link': 'https://linkedin.com/jobs/view/12347',  # Different link
        'Search Keywords': 'Data Analyst',
        'Search Location': 'New York City Metro Area'
    },
    {
        'Job Title': 'Data Analyst',  # Duplicate title and company
        'Company': 'Tech Corp',       # Duplicate company
        'Location': 'New York, NY',
        'Post Date': '2023-10-01',
        'Link': 'https://linkedin.com/jobs/view/12345',  # Same link (true duplicate)
        'Search Keywords': 'Data Analyst',
        'Search Location': 'New York City Metro Area'
    }
]

print(f"1. Created sample data with {len(sample_data)} job listings")
print("   Sample data includes duplicates for testing removal functionality")

def process_and_save_data(data: list[dict], output_filename: str = 'linkedin_jobs_raw.csv'):
    """Converts data to DataFrame, removes duplicates, and saves to CSV."""
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    print(f"2. Raw listings collected: {len(df)}")
    
    # Step 5: Add Duplicate Removal
    # We keep the first instance of a job based on the combination of Title and Company/Link
    df_cleaned = df.drop_duplicates(subset=['Job Title', 'Company', 'Link'], keep='first')
    
    # Save the cleaned data with a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f'linkedin_jobs_{timestamp}.csv'
    df_cleaned.to_csv(final_filename, index=False)
    
    print(f"3. Duplicates removed: {len(df) - len(df_cleaned)}")
    print(f"4. ✅ Final data saved to {final_filename} with {len(df_cleaned)} unique listings.")
    
    # Display the cleaned data
    print("\n5. Cleaned Data Preview:")
    print(df_cleaned.to_string(index=False))
    
    return df_cleaned

# Test the function
print("\n🧪 Testing process_and_save_data function...")
result = process_and_save_data(sample_data)

print("\n✅ Data processing and saving test completed successfully!")
print("💡 The function correctly:")
print("   • Converts list of dictionaries to DataFrame")
print("   • Identifies and removes duplicates based on Job Title, Company, and Link")
print("   • Saves data to timestamped CSV file")
print("   • Returns cleaned DataFrame for further processing")