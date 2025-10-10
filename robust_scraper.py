from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import time
import getpass
import sys
import os
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

def create_driver():
    """Create and configure Chrome WebDriver with robust settings"""
    try:
        print("🔧 Configuring Chrome WebDriver...")
        
        # Define Chrome Options for anti-detection and stability
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) 
        chrome_options.add_argument("--window-size=1280,800")
        
        # Essential anti-detection flags
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Stability flags to handle connection issues
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-background-networking")
        
        # User Agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        print("🔄 Attempting to auto-install/load ChromeDriver...")
        
        # Use webdriver_manager to get the perfect Service instance
        service = Service(ChromeDriverManager().install())
        service.log_path = "chromedriver.log"  # Enable logging
        
        # Create driver with increased timeout
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(60)  # Increase timeout
        driver.implicitly_wait(10)
        
        print("✅ WebDriver initialized successfully.")
        return driver
        
    except Exception as e:
        print(f"❌ Critical WebDriver Error: {e}")
        print("💡 Troubleshooting tips:")
        print("   1. Make sure Chrome is updated to the latest version")
        print("   2. Try restarting your computer")
        print("   3. Check if any antivirus is blocking the connection")
        print("   4. Try running the script as administrator")
        return None

def apply_anti_detection(driver):
    """Apply anti-detection measures"""
    try:
        # Execute CDP command to hide WebDriver
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
            """
        })
        print("✅ Anti-detection measures applied successfully.")
        return True
    except Exception as e:
        print(f"⚠️ Failed to apply anti-detection measures: {e}")
        return False

def safe_navigate(driver, url, max_retries=3):
    """Safely navigate to a URL with retries"""
    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempting to load {url} (attempt {attempt + 1}/{max_retries})...")
            driver.get(url)
            print(f"✅ Page loaded successfully: {driver.title}")
            return True
        except TimeoutException:
            print(f"⚠️ Timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                print("⏳ Waiting 5 seconds before retry...")
                time.sleep(5)
        except WebDriverException as e:
            print(f"⚠️ WebDriver error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print("⏳ Waiting 5 seconds before retry...")
                time.sleep(5)
        except Exception as e:
            print(f"⚠️ Unexpected error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print("⏳ Waiting 5 seconds before retry...")
                time.sleep(5)
    
    print(f"❌ Failed to load {url} after {max_retries} attempts")
    return False

def linkedin_login(driver, email, password):
    """Navigates to LinkedIn login and attempts to sign in."""
    if not safe_navigate(driver, "https://www.linkedin.com/login"):
        return False
        
    wait = WebDriverWait(driver, 20)  # Increased timeout

    try:
        # 1. Fill Username
        print("📝 Filling username...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(email)

        # 2. Fill Password
        print("📝 Filling password...")
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)

        # 3. Click Login Button
        print("🚀 Clicking login button...")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']")))
        login_button.click()

        print("⏳ Waiting for login to complete...")

        # 4. Wait for successful post-login element (e.g., the global search bar)
        wait.until(EC.presence_of_element_located((By.ID, "global-nav-typeahead")))
        print("✅ Successfully logged into LinkedIn.")
        return True

    except Exception as e:
        print(f"❌ Login failed! Error: {e}")
        return False

def navigate_to_jobs(driver, keywords, location):
    """Constructs the job search URL and navigates the browser."""
    
    # Simple URL encoding (replacing spaces with %20)
    keywords_encoded = keywords.replace(' ', '%20')
    location_encoded = location.replace(' ', '%20')

    # Construct the search URL
    jobs_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords_encoded}&location={location_encoded}"

    if safe_navigate(driver, jobs_url):
        wait = WebDriverWait(driver, 20)
        # Wait for the main job results container to ensure the page is loaded
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
            print(f"✅ Job search results page loaded for '{keywords}' in '{location}'.")
            return jobs_url
        except Exception as e:
            print(f"❌ Failed to load job search results page: {e}")
            return None
    return None

def scroll_and_scrape_jobs(driver, max_scrolls=3):
    """Scrolls through the job listings and extracts job data using BeautifulSoup."""
    # Wait for job results to load
    wait = WebDriverWait(driver, 20)
    try:
        job_list_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
    except TimeoutException:
        print("❌ Job results container not found.")
        return []
    
    # Execute JavaScript to get the height of the scrollable area
    last_height = driver.execute_script("return arguments[0].scrollHeight;", job_list_container)
    scrolls = 0
    job_data = []

    print("🔍 Starting to scroll and collect job data...")
    
    while scrolls < max_scrolls:
        # Scroll to the bottom of the job list container
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", job_list_container)
        
        # Wait for new jobs to load
        time.sleep(5)  # Increased wait time
        
        # Check if we've reached the end of the scrollable area
        new_height = driver.execute_script("return arguments[0].scrollHeight;", job_list_container)
        if new_height == last_height:
            print("Reached the end of job listings.")
            break
            
        last_height = new_height
        scrolls += 1
        
        print(f"Completed scroll {scrolls}/{max_scrolls}")
    
    # After scrolling, extract job data
    print("📄 Extracting job data with BeautifulSoup...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find job cards - LinkedIn's structure may vary, so we'll look for common classes
    job_cards = soup.find_all('li', class_='jobs-search-results__list-item')
    
    if not job_cards:
        # Try alternative selector
        job_cards = soup.find_all('div', {'data-job-id': True})
        
    if not job_cards:
        # Try another alternative selector
        job_cards = soup.find_all('a', class_='base-card__full-link')
    
    print(f"Found {len(job_cards)} job cards.")
    
    for card in job_cards:
        try:
            # Extract job title
            title_elem = card.find('h3', class_='base-search-card__title') or card.find('a', class_='job-card-list__title') or card.find('span', class_='sr-only')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Extract company name
            company_elem = card.find('h4', class_='base-search-card__subtitle') or card.find('a', class_='job-card-container__company-name') or card.find('a', class_='hidden-nested-link')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Extract location
            location_elem = card.find('span', class_='job-search-card__location') or card.find('span', class_='job-result-card__location')
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Extract job link
            link_elem = card.find('a', class_='base-card__full-link') or card.find('a', class_='job-card-list__title') or card
            link = ""
            if link_elem.has_attr('href'):
                link = link_elem['href']
            elif link_elem.name == 'a':
                link = link_elem.get('href', '')
            else:
                # Look for href in parent elements
                parent_link = link_elem.find_parent('a')
                if parent_link and parent_link.has_attr('href'):
                    link = parent_link['href']
            
            # If still no link, try to construct from job id
            if not link or link == "N/A":
                job_id = card.get('data-job-id') or card.get('data-entity-urn')
                if job_id:
                    link = f"https://www.linkedin.com/jobs/view/{job_id}"
            
            job_data.append({
                'title': title,
                'company': company,
                'location': location,
                'link': link if link else "N/A"
            })
        except Exception as e:
            print(f"Error parsing job card: {e}")
            continue
    
    return job_data

def main():
    print("🚀 Starting LinkedIn Job Scraper...")
    print("=" * 50)
    
    # Create driver
    driver = create_driver()
    if not driver:
        print("❌ Failed to create WebDriver. Exiting.")
        return
    
    try:
        # Apply anti-detection measures
        apply_anti_detection(driver)
        
        # Get credentials
        email, password = prompt_linkedin_credentials()
        if email is None or password is None:
            print("❌ Error: Missing credentials.")
            return

        # Login to LinkedIn
        print("\n🔐 Attempting LinkedIn login...")
        if linkedin_login(driver, email, password):
            print("\n🎯 Navigating to job search...")
            search_term = "Data Analyst"
            location = "New York City Metro Area"
            
            url = navigate_to_jobs(driver, keywords=search_term, location=location)
            if url:
                print(f"\n📊 Scraping job listings...")
                job_data = scroll_and_scrape_jobs(driver, max_scrolls=3)
                print(f"\n📈 Extracted {len(job_data)} job listings:")
                for i, job in enumerate(job_data[:10], 1):  # Show first 10 jobs
                    print(f"\n{i}. {job['title']}")
                    print(f"   Company: {job['company']}")
                    print(f"   Location: {job['location']}")
                    print(f"   Link: {job['link']}")
            
            # Pause for visibility before the script ends
            print(f"\n⏳ Keeping browser open for 30 seconds for inspection...")
            time.sleep(30)
            print("✅ Script completed.")
        else:
            print("❌ LinkedIn login failed.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Script interrupted by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        print("🏁 Script finished.")

if __name__ == "__main__":
    main()