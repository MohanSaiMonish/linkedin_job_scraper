import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from collections import Counter
import getpass
import os

def setup_driver():
    """Set up Chrome WebDriver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Execute script to mask automation
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def login_linkedin(driver, email, password):
    """Log into LinkedIn"""
    driver.get("https://www.linkedin.com/login")
    
    # Wait for page to load and find email field
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_field.send_keys(email)
    
    # Find password field and enter password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    
    # Click login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    
    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "global-nav-typeahead"))
    )
    print("✅ Successfully logged into LinkedIn")

def search_jobs(driver, keywords, location):
    """Search for jobs on LinkedIn"""
    # Navigate to jobs page
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(2)
    
    # Find and fill keywords
    keywords_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword')]"))
    )
    keywords_input.clear()
    keywords_input.send_keys(keywords)
    
    # Find and fill location
    location_input = driver.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-location')]")
    location_input.clear()
    location_input.send_keys(location)
    
    # Submit search
    search_button = driver.find_element(By.XPATH, "//button[@data-tracking-control-name='public_jobs_jobs-search-bar_base-search-bar-search-submit']")
    search_button.click()
    
    # Wait for results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
    )
    print(f"✅ Found jobs for '{keywords}' in '{location}'")

def scroll_jobs_list(driver, scroll_pause_time=2, max_scrolls=5):
    """Scroll through jobs list to load more results"""
    # Get scroll container
    scroll_container = driver.find_element(By.CLASS_NAME, "jobs-search-results-list")
    
    # Get initial scroll height
    last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
    
    scrolls = 0
    while scrolls < max_scrolls:
        # Scroll to bottom
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", scroll_container)
        
        # Wait for new content to load
        time.sleep(scroll_pause_time)
        
        # Check new scroll height
        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
        
        # If no new content, break
        if new_height == last_height:
            break
            
        last_height = new_height
        scrolls += 1
        print(f"Scrolled {scrolls}/{max_scrolls} times")

def extract_job_data(driver):
    """Extract job data using BeautifulSoup"""
    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find job cards
    job_cards = soup.find_all('div', class_='job-card-container')
    
    jobs_data = []
    
    for card in job_cards:
        try:
            # Extract job title
            title_elem = card.find('a', class_='job-card-list__title')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Extract company name
            company_elem = card.find('a', class_='job-card-container__company-name')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Extract location
            location_elem = card.find('li', class_='job-card-container__metadata-item')
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Extract post date
            date_elem = card.find('time')
            post_date = date_elem.get('datetime') if date_elem else "N/A"
            
            # Extract job link
            link = title_elem.get('href') if title_elem else "N/A"
            if link != "N/A":
                link = f"https://www.linkedin.com{link}"
            
            jobs_data.append({
                'Job Title': title,
                'Company': company,
                'Location': location,
                'Post Date': post_date,
                'Link': link
            })
        except Exception as e:
            print(f"Error extracting job data: {e}")
            continue
    
    print(f"✅ Extracted {len(jobs_data)} job listings")
    return jobs_data

def save_to_csv(data, filename='linkedin_jobs.csv'):
    """Save job data to CSV file"""
    if not data:
        print("No data to save")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Remove duplicates based on job title and company
    df_cleaned = df.drop_duplicates(subset=['Job Title', 'Company'], keep='first')
    
    # Save to CSV
    df_cleaned.to_csv(filename, index=False)
    print(f"✅ Saved {len(df_cleaned)} jobs to {filename}")
    return df_cleaned

def visualize_job_frequency(df, filename='company_job_frequency.png'):
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

def main():
    """Main function to run the LinkedIn job scraper"""
    print("🚀 Starting LinkedIn Job Scraper")
    
    # Get credentials
    email = input("Enter your LinkedIn email: ")
    password = getpass.getpass("Enter your LinkedIn password: ")
    
    # Get search parameters
    keywords = input("Enter job keywords (e.g., 'Data Analyst'): ") or "Data Analyst"
    location = input("Enter job location (e.g., 'New York'): ") or "New York"
    
    driver = None
    try:
        # Set up driver
        print("🔧 Setting up WebDriver...")
        driver = setup_driver()
        
        # Login to LinkedIn
        print("🔐 Logging into LinkedIn...")
        login_linkedin(driver, email, password)
        
        # Search for jobs
        print("🔍 Searching for jobs...")
        search_jobs(driver, keywords, location)
        
        # Scroll to load more jobs
        print("🖱️  Scrolling to load more jobs...")
        scroll_jobs_list(driver, max_scrolls=3)
        
        # Extract job data
        print("📊 Extracting job data...")
        jobs_data = extract_job_data(driver)
        
        # Save to CSV
        print("💾 Saving to CSV...")
        df = save_to_csv(jobs_data)
        
        # Create visualization
        if df is not None and not df.empty:
            print("📈 Creating visualization...")
            visualize_job_frequency(df)
        
        print("✅ Job scraping completed successfully!")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    finally:
        # Close the driver
        if driver:
            driver.quit()
            print("🔒 WebDriver closed")

if __name__ == "__main__":
    main()