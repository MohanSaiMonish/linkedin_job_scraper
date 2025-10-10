from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import getpass
import sys
import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
PROJECT_DIR = Path(__file__).parent
load_dotenv(PROJECT_DIR / ".env")

# --- Core Functions ---

def prompt_linkedin_credentials():
    """Fetches credentials from env vars or prompts securely if missing."""
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    if email and password:
        return email, password
    try:
        email = input("Enter your LinkedIn email: ") if not email else email
        password = getpass.getpass("Enter your LinkedIn password: ") if not password else password
        return email, password
    except Exception as e:
        print(f"Error getting input: {e}")
        return None, None

def linkedin_login(driver, email, password):
    """Navigates to LinkedIn login and attempts to sign in."""
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 15)

    try:
        # 1. Fill Username
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(email)

        # 2. Fill Password
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)

        # 3. Click Login Button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']")))
        login_button.click()

        print("Login attempt initiated...")

        # 4. Wait for successful post-login element (e.g., the global search bar)
        wait.until(EC.presence_of_element_located((By.ID, "global-nav-typeahead")))
        print("✅ Successfully logged into LinkedIn.")
        return True

    except Exception as e:
        print(f"❌ Login failed! Check credentials or selectors. Error: {e}")
        return False

def navigate_to_jobs(driver, keywords, location):
    """Constructs the job search URL and navigates the browser."""
    
    # Simple URL encoding (replacing spaces with %20)
    keywords_encoded = keywords.replace(' ', '%20')
    location_encoded = location.replace(' ', '%20')

    # Construct the search URL
    jobs_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords_encoded}&location={location_encoded}"

    driver.get(jobs_url)
    wait = WebDriverWait(driver, 15)
    
    # Wait for the main job results container to ensure the page is loaded
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
        print(f"✅ Job search results page loaded for '{keywords}' in '{location}'.")
        return jobs_url
    except Exception as e:
        print(f"❌ Failed to load job search results page: {e}")
        return None

# --- NEW Core Scraper Function ---
def scrape_jobs(driver: webdriver.Chrome, keywords: str, location: str):
    """Scrolls through the job listings and extracts job data using BeautifulSoup."""
    # Wait for job results to load
    wait = WebDriverWait(driver, 15)
    try:
        # Find the job results scroll pane element
        results_pane = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list"))
        )
        print("✅ Job results panel found.")
    except TimeoutException:
        print("❌ Job results container not found.")
        return []

    # Scroll the job results panel to load all listings
    print("🔍 Starting scroll and job collection...")
    
    scroll_count = 0
    max_scrolls = 5  # Adjust this number based on how many jobs you want to collect
    
    while scroll_count < max_scrolls:
        # Scroll down within the results pane
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_pane)
        time.sleep(2)  # Give time for new listings to load
        scroll_count += 1
        print(f"Scrolled {scroll_count} times...")
        
    # Get the full page source after scrolling
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # List to hold all scraped job data
    data = []
    
    # Find all job card containers
    # Try multiple selectors to accommodate LinkedIn's changing UI
    job_cards = soup.find_all('div', class_='job-card-container--clickable') 
    
    if not job_cards:
        # Fallback selectors
        job_cards = soup.find_all('li', class_='jobs-search-results__list-item')
        
    if not job_cards:
        # Another fallback
        job_cards = soup.find_all('div', {'data-job-id': True})
    
    print(f"Found {len(job_cards)} job cards on the page.")

    for card in job_cards:
        try:
            # Locate job title, company, and post date within each card
            title_el = card.find('h3', class_='base-search-card__title')
            company_el = card.find('h4', class_='base-search-card__subtitle')
            location_el = card.find('span', class_='job-search-card__location')
            date_el = card.find('time', class_='job-search-card__listdate')
            link_el = card.find('a', class_='base-card__full-link')

            # Extract text and link, handling potential missing elements
            title = title_el.text.strip() if title_el else 'N/A'
            company = company_el.text.strip() if company_el else 'N/A'
            location = location_el.text.strip() if location_el else 'N/A'
            post_date = date_el['datetime'].strip() if date_el and 'datetime' in date_el.attrs else (date_el.text.strip() if date_el else 'N/A')
            job_link = link_el['href'].split('?')[0] if link_el else 'N/A'  # Clean up the link

            data.append({
                'Job Title': title,
                'Company': company,
                'Location': location,
                'Post Date': post_date,
                'Link': job_link,
                'Search Keywords': keywords,
                'Search Location': location
            })
        except Exception as e:
            # Skip any card that causes an unexpected error during parsing
            print(f"Skipping job card due to error: {e}")
            continue
            
    return data

def process_and_save_data(data: list[dict], output_filename: str = 'linkedin_jobs_raw.csv'):
    """Converts data to DataFrame, removes duplicates, and saves to CSV."""
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    print(f"Raw listings collected: {len(df)}")
    
    # Step 5: Add Duplicate Removal
    # We keep the first instance of a job based on the combination of Title and Company/Link
    # Handle both data formats (old and new)
    if 'Job Title' in df.columns:
        # New format
        df_cleaned = df.drop_duplicates(subset=['Job Title', 'Company', 'Link'], keep='first')
    else:
        # Old format
        df_cleaned = df.drop_duplicates(subset=['title', 'company', 'link'], keep='first')
    
    # Save the cleaned data with a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f'linkedin_jobs_{timestamp}.csv'
    df_cleaned.to_csv(final_filename, index=False)
    
    print(f"Duplicates removed: {len(df) - len(df_cleaned)}")
    print(f"✅ Final data saved to {final_filename} with {len(df_cleaned)} unique listings.")
    
    return df_cleaned

if __name__ == "__main__":
    
    # Define job search parameters
    search_term = "Data Analyst"
    location = "New York City Metro Area"

    driver = None
    try:
        # --- 1. WebDriver Setup (reusing your setup logic) ---
        # NOTE: If running visibly, ensure you remove the driver.quit() line until you're done debugging!
        # This block needs to be updated to match the final driver setup you're using.
        # Assuming the driver setup from the last exchange is working:
        
        # --- Simplified Setup for Demo ---
        # We will assume get_driver() (or similar function) is defined and handles options/fallbacks.
        # Since the interface wasn't opening, ensure HEADLESS=False or remove the flag for debugging.
        
        # --- Using the most recent (complex) setup logic ---
        # The full setup block from your last exchange should be placed here.
        # (To keep it clean, let's use the function from a previous Cursor turn that defines Options)
        
        # Create Options for visible mode
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) # Keep window open after script ends
        chrome_options.add_argument("--window-size=1280,800")
        
        # Anti-Detection Flags
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Stability Flags
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # User Agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        print("Attempting to auto-install/load ChromeDriver...")
        
        # If the local driver failed, we must install the manager dependency:
        S = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=S, options=chrome_options)
        driver.set_page_load_timeout(45)
        print("✅ WebDriver initialized successfully. Browser should be open.")

        # Run the CDP tweak script immediately after driver initialization
        try:
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
        except Exception:
            pass
        
        # --- 2. Login and Navigation ---
        email, password = prompt_linkedin_credentials()
        if not email or not password:
            sys.exit(1)
        
        if linkedin_login(driver, email, password):
            url = navigate_to_jobs(driver, keywords=search_term, location=location)
            print(f"Navigating to: {url}")
            
            # --- 3. Scraping, Processing, and Saving ---
            if url:
                scraped_data = scrape_jobs(driver, search_term, location)
                
                # Step 4, 5: Process and Save
                if scraped_data:
                    process_and_save_data(scraped_data)
                else:
                    print("No data was scraped.")
            else:
                print("Failed to navigate to job search page.")
        else:
            print("Login failed.")

    except Exception as e:
        print(f"A critical error occurred: {e}")
        import traceback
        traceback.print_exc()
        # Optionally save a screenshot here for debugging the failure
        
    finally:
        # NOTE: We keep driver.quit() commented out temporarily to aid debugging
        # driver.quit() 
        print("Script finished. Check the browser window for final status (if detached).")
