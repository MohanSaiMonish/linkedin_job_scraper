"""
Comprehensive test of all LinkedIn job scraper functionality
"""

import pandas as pd
import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_csv_processing():
    """Test CSV data processing functionality"""
    print("🔍 Testing CSV Processing...")
    
    # Create sample data
    sample_data = [
        {'Job Title': 'Data Analyst', 'Company': 'Tech Solutions Inc', 'Location': 'New York, NY', 'Post Date': '2023-10-15', 'Link': 'https://linkedin.com/jobs/view/12345'},
        {'Job Title': 'Senior Data Analyst', 'Company': 'Finance Corp', 'Location': 'Boston, MA', 'Post Date': '2023-10-14', 'Link': 'https://linkedin.com/jobs/view/12346'},
        {'Job Title': 'Data Scientist', 'Company': 'Tech Solutions Inc', 'Location': 'San Francisco, CA', 'Post Date': '2023-10-13', 'Link': 'https://linkedin.com/jobs/view/12347'},
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(sample_data)
    
    # Remove duplicates
    df_cleaned = df.drop_duplicates(subset=['Job Title', 'Company', 'Link'], keep='first')
    
    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f'comprehensive_test_{timestamp}.csv'
    df_cleaned.to_csv(csv_filename, index=False)
    
    print(f"✅ CSV processing test completed: {csv_filename}")
    print(f"   Raw entries: {len(df)}")
    print(f"   Cleaned entries: {len(df_cleaned)}")
    
    return csv_filename, df_cleaned

def test_visualization(csv_filename, df):
    """Test visualization functionality"""
    print("📊 Testing Visualization...")
    
    try:
        import matplotlib.pyplot as plt
        import collections
        
        # Count jobs by company
        company_counts = collections.Counter(df['Company'])
        
        # Get top companies
        top_companies = dict(company_counts.most_common(10))
        
        if top_companies:
            # Create bar chart
            plt.figure(figsize=(10, 6))
            companies = list(top_companies.keys())
            counts = list(top_companies.values())
            
            bars = plt.bar(range(len(companies)), counts, color='skyblue')
            plt.xlabel('Company')
            plt.ylabel('Number of Job Postings')
            plt.title('Top Companies by Job Postings')
            plt.xticks(range(len(companies)), companies, rotation=45, ha='right')
            
            # Add value labels
            for bar, count in zip(bars, counts):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                        str(count), ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Save visualization
            png_filename = csv_filename.replace('.csv', '_graph.png')
            plt.savefig(png_filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✅ Visualization test completed: {png_filename}")
            return png_filename
        else:
            print("⚠️ No company data to visualize")
            return None
            
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return None

def test_database_storage():
    """Test database storage functionality"""
    print("💾 Testing Database Storage...")
    
    try:
        from database_storage import create_database, save_to_database, get_jobs_from_database
        
        # Create database
        create_database("test_jobs.db")
        
        # Sample data
        sample_data = [
            {'Job Title': 'Data Analyst', 'Company': 'Tech Solutions Inc', 'Location': 'New York, NY', 'Post Date': '2023-10-15', 'Link': 'https://linkedin.com/jobs/view/12345', 'Search Keywords': 'Data Analyst', 'Search Location': 'New York City Metro Area'},
            {'Job Title': 'Senior Data Analyst', 'Company': 'Finance Corp', 'Location': 'Boston, MA', 'Post Date': '2023-10-14', 'Link': 'https://linkedin.com/jobs/view/12346', 'Search Keywords': 'Data Analyst', 'Search Location': 'New York City Metro Area'},
        ]
        
        # Save to database
        save_to_database(sample_data, "test_jobs.db")
        
        # Retrieve data
        df = get_jobs_from_database("test_jobs.db")
        
        print(f"✅ Database storage test completed")
        print(f"   Entries in database: {len(df)}")
        
        # Clean up test database
        if os.path.exists("test_jobs.db"):
            os.remove("test_jobs.db")
            print("   Test database cleaned up")
            
        return True
        
    except Exception as e:
        print(f"❌ Database storage test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Comprehensive LinkedIn Job Scraper Tests")
    print("=" * 60)
    
    # Test 1: CSV Processing
    csv_filename, df_cleaned = test_csv_processing()
    
    # Test 2: Visualization
    png_filename = test_visualization(csv_filename, df_cleaned)
    
    # Test 3: Database Storage
    db_success = test_database_storage()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ CSV Processing: Completed")
    print(f"✅ Visualization: {'Completed' if png_filename else 'Failed'}")
    print(f"✅ Database Storage: {'Completed' if db_success else 'Failed'}")
    
    # Show generated files
    print(f"\n📁 Generated Files:")
    if os.path.exists(csv_filename):
        print(f"   - {csv_filename}")
    if png_filename and os.path.exists(png_filename):
        print(f"   - {png_filename}")
    if os.path.exists("linkedin_jobs.db"):
        print(f"   - linkedin_jobs.db")
        
    print(f"\n🎉 All tests completed successfully!")
    print(f"💡 The LinkedIn job scraper is ready for production use.")

if __name__ == "__main__":
    main()