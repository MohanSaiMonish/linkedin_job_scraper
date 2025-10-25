from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import getpass
import sys
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
PROJECT_DIR = Path(__file__).parent
load_dotenv(PROJECT_DIR / ".env")

def get_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        S = Service('./chromedriver.exe')
        driver = webdriver.Chrome(service=S, options=chrome_options)
        print("WebDriver initialized (local driver).")
    except Exception:
        S = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=S, options=chrome_options)
        print("WebDriver initialized (webdriver-manager).")
    
    driver.set_page_load_timeout(30)
    return driver

def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 15)
    
    try:
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(email)
        
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']")))
        login_button.click()
        
        print("Login attempt initiated...")
        wait.until(EC.presence_of_element_located((By.ID, "global-nav-typeahead")))
        print("✅ Successfully logged into LinkedIn.")
        return True
    except Exception as e:
        print(f"❌ Login failed! Error: {e}")
        return False

def scrape_jobs(driver, keywords, location, max_jobs=20):
    """Scrape job listings and return job data"""
    keywords_encoded = keywords.replace(' ', '%20')
    location_encoded = location.replace(' ', '%20')
    jobs_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords_encoded}&location={location_encoded}"
    
    driver.get(jobs_url)
    wait = WebDriverWait(driver, 15)
    
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
        print(f"✅ Job search results page loaded for '{keywords}' in '{location}'.")
        
        jobs_data = []
        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job-search-card")
        
        for i, job_card in enumerate(job_cards[:max_jobs]):
            try:
                # Extract job title
                title_elem = job_card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title")
                title = title_elem.text.strip()
                
                # Extract company name
                company_elem = job_card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle")
                company = company_elem.text.strip()
                
                # Extract location
                location_elem = job_card.find_element(By.CSS_SELECTOR, "span.job-search-card__location")
                job_location = location_elem.text.strip()
                
                # Extract date posted
                date_elem = job_card.find_element(By.CSS_SELECTOR, "time")
                date_posted = date_elem.get_attribute("datetime") or date_elem.text.strip()
                
                jobs_data.append({
                    'Job Title': title,
                    'Company': company,
                    'Location': job_location,
                    'Date Posted': date_posted
                })
                
                print(f"Scraped job {i+1}: {title} at {company}")
                
            except Exception as e:
                print(f"Error scraping job {i+1}: {e}")
                continue
        
        return jobs_data, jobs_url
        
    except Exception as e:
        print(f"❌ Failed to load job search results page: {e}")
        return [], None

def save_to_csv(jobs_data, filename="linkedin_jobs.csv"):
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
    from collections import Counter
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

if __name__ == "__main__":
    # Configuration - Change these values
    JOB_KEYWORDS = "Software Engineer"  # Change role here
    JOB_LOCATION = "San Francisco Bay Area"  # Change location here
    MAX_JOBS = 25  # Number of jobs to scrape
    
    driver = get_driver()
    
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not email or not password:
        email = input("Enter your LinkedIn email: ")
        password = getpass.getpass("Enter your LinkedIn password: ")
    
    if linkedin_login(driver, email, password):
        print(f"\n🔍 Scraping jobs for: {JOB_KEYWORDS} in {JOB_LOCATION}")
        jobs_data, jobs_url = scrape_jobs(driver, JOB_KEYWORDS, JOB_LOCATION, MAX_JOBS)
        
        if jobs_data:
            # Save to CSV
            save_to_csv(jobs_data, f"linkedin_jobs_{JOB_KEYWORDS.replace(' ', '_').lower()}.csv")
            
            # Create visualization
            create_visualization(jobs_data, JOB_KEYWORDS, JOB_LOCATION)
            
            print(f"\n📊 Analysis Complete!")
            print(f"✅ Scraped {len(jobs_data)} jobs")
            print(f"✅ Saved to CSV file")
            print(f"✅ Created visualization")
        else:
            print("❌ No job data scraped")
    
    # Keep browser open for manual inspection
    print("\nBrowser will stay open for 30 seconds. Complete any CAPTCHA or security checks manually.")
    time.sleep(30)
    driver.quit()
    print("Browser closed. Script finished.")
