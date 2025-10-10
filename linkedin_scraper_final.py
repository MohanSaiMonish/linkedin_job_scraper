from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import os

def create_driver():
    """Create and configure the Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Keep window open after script ends
    chrome_options.add_argument("--window-size=1920,1080")
    
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
    chrome_options.add_argument("--lang=en-US")
    
    # User Agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    print("🔧 Installing/finding ChromeDriver...")
    
    # Auto-install ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    
    # Execute CDP commands to mask automation
    try:
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = {runtime: {}};
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
            """
        })
    except Exception as e:
        print(f"⚠️ Warning: Could not execute CDP command: {e}")
    
    return driver

def check_and_wait_for_login(driver):
    """Check if logged in, if not wait for manual login"""
    print("🔍 Checking login status...")
    
    # Check current page
    if "linkedin.com/feed" in driver.current_url or "linkedin.com/in/" in driver.current_url:
        print("✅ Already logged into LinkedIn")
        return True
    
    if "linkedin.com/login" in driver.current_url or "linkedin.com/uas/login" in driver.current_url:
        print("❌ Not logged into LinkedIn")
        print("📝 Please log in manually in the browser window")
        print("⏳ Waiting for you to log in...")
        
        # Wait for login by checking URL changes
        start_time = time.time()
        timeout = 120  # 2 minutes timeout
        
        while time.time() - start_time < timeout:
            if "linkedin.com/feed" in driver.current_url or "linkedin.com/in/" in driver.current_url:
                print("✅ Login detected!")
                return True
            time.sleep(2)
        
        print("⏰ Timeout waiting for login")
        return False
    
    # If on homepage, check for login elements
    try:
        sign_in_button = driver.find_element(By.XPATH, "//a[contains(@href, '/login')]")
        print("❌ Not logged in - found sign in button")
        print("📝 Please log in manually in the browser window")
        print("⏳ Waiting for you to log in...")
        
        # Wait for login by checking URL changes
        start_time = time.time()
        timeout = 120  # 2 minutes timeout
        
        while time.time() - start_time < timeout:
            if "linkedin.com/feed" in driver.current_url or "linkedin.com/in/" in driver.current_url:
                print("✅ Login detected!")
                return True
            time.sleep(2)
            
        print("⏰ Timeout waiting for login")
        return False
    except:
        print("✅ Appears to be logged in")
        return True

def navigate_to_search(driver, keywords="Data Analyst", location="New York City Metro Area"):
    """Navigate directly to job search results"""
    # URL encode search terms
    keywords_encoded = keywords.replace(' ', '%20')
    location_encoded = location.replace(' ', '%20')
    
    # Direct URL to job search
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords_encoded}&location={location_encoded}"
    
    print(f"🧭 Navigating to job search: {search_url}")
    driver.get(search_url)
    
    # Wait for job results to load
    wait = WebDriverWait(driver, 20)
    try:
        results_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list"))
        )
        print("✅ Job search results loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to load job search results: {e}")
        # Print current URL and title for debugging
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        return False

def scroll_job_results(driver, max_scrolls=5):
    """Enhanced scroll through job results to load more listings"""
    print("🔍 Starting enhanced scroll operations...")
    
    try:
        # Find the scrollable results pane
        results_pane = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list"))
        )
        
        # Get initial scroll height
        last_height = driver.execute_script("return arguments[0].scrollHeight", results_pane)
        print(f"📊 Initial scroll height: {last_height}")
        
        scroll_count = 0
        consecutive_same_height = 0
        max_consecutive_same = 3
        
        while scroll_count < max_scrolls and consecutive_same_height < max_consecutive_same:
            # Scroll to bottom of results pane
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_pane)
            print(f"⬇️ Scroll #{scroll_count + 1} completed")
            
            # Wait for new content to load (increased time)
            time.sleep(4)
            
            # Check new scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight", results_pane)
            print(f"📊 New scroll height: {new_height}")
            
            # If height didn't change, increment counter
            if new_height == last_height:
                consecutive_same_height += 1
                print(f"⚠️ Height unchanged ({consecutive_same_height}/{max_consecutive_same})")
            else:
                consecutive_same_height = 0  # Reset counter
                
            last_height = new_height
            scroll_count += 1
            
        print(f"✅ Completed {scroll_count} scroll operations")
        return True
        
    except Exception as e:
        print(f"❌ Error during scrolling: {e}")
        import traceback
        traceback.print_exc()
        return False

def extract_job_data(driver):
    """Extract job data using multiple strategies"""
    print("🔍 Extracting job data with multiple strategies...")
    
    # Wait a bit for content to settle
    time.sleep(2)
    
    # Get page source after scrolling
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Try multiple strategies to find job cards
    job_cards = []
    
    # Strategy 1: Main job card container
    cards = soup.find_all('div', class_='job-card-container')
    if cards:
        job_cards.extend(cards)
        print(f"✅ Found {len(cards)} job cards with 'job-card-container'")
    
    # Strategy 2: List item approach
    if not job_cards:
        cards = soup.find_all('li', class_='jobs-search-results__list-item')
        if cards:
            job_cards.extend(cards)
            print(f"✅ Found {len(cards)} job cards with 'jobs-search-results__list-item'")
    
    # Strategy 3: Data attribute approach
    if not job_cards:
        cards = soup.find_all('div', {'data-job-id': True})
        if cards:
            job_cards.extend(cards)
            print(f"✅ Found {len(cards)} job cards with 'data-job-id'")
    
    # Strategy 4: Any job card link
    if not job_cards:
        cards = soup.find_all('a', class_='job-card-list__title')
        if cards:
            # Get parent containers
            for card_link in cards:
                parent = card_link.find_parent('div', class_='job-card-container')
                if parent and parent not in job_cards:
                    job_cards.append(parent)
            print(f"✅ Found {len(job_cards)} job cards by parent search")
    
    print(f"📊 Total job cards found: {len(job_cards)}")
    
    if not job_cards:
        # Print a portion of the page source for debugging
        print("❌ No job cards found. Printing first 2000 chars of page source for debugging:")
        print("="*50)
        print(driver.page_source[:2000])
        print("="*50)
        return []
    
    data = []
    for i, card in enumerate(job_cards):
        try:
            # Multiple strategies for each data point
            # Job Title
            title_elem = (card.find('a', class_='job-card-list__title') or 
                         card.find('h3', class_='base-search-card__title') or
                         card.find('span', class_='sr-only') or
                         card.find('a', {'data-tracking-control-name': 'public_jobs_jserp-result_search-card'}))
            
            # Company Name
            company_elem = (card.find('a', class_='job-card-container__company-name') or
                           card.find('h4', class_='base-search-card__subtitle') or
                           card.find('a', class_='hidden-nested-link') or
                           card.find('span', class_='job-card-container__primary-description'))
            
            # Location
            location_elem = (card.find('span', class_='job-card-container__metadata-item') or
                            card.find('span', class_='job-search-card__location') or
                            card.find('li', class_='job-card-container__metadata-item') or
                            card.find('span', class_='job-card-container__workplace-type'))
            
            # Post Date
            date_elem = card.find('time')
            
            # Job Link
            link_elem = (card.find('a', class_='job-card-list__title') or
                        card.find('a', class_='base-card__full-link') or
                        card.find('a', href=lambda x: x and '/jobs/view/' in x))
            
            # Extract text with fallbacks
            title = title_elem.get_text(strip=True) if title_elem else 'N/A'
            company = company_elem.get_text(strip=True) if company_elem else 'N/A'
            location = location_elem.get_text(strip=True) if location_elem else 'N/A'
            post_date = date_elem.get('datetime', '') if date_elem and date_elem.get('datetime') else (date_elem.get_text(strip=True) if date_elem else 'N/A')
            job_link = link_elem.get('href', 'N/A') if link_elem else 'N/A'
            
            # Clean up link
            if job_link != 'N/A':
                # Handle relative links
                if job_link.startswith('/'):
                    job_link = 'https://www.linkedin.com' + job_link
                # Remove tracking parameters
                if '?' in job_link:
                    job_link = job_link.split('?')[0]
            
            # Only add if we have a title
            if title != 'N/A':
                data.append({
                    'Job Title': title,
                    'Company': company,
                    'Location': location,
                    'Post Date': post_date,
                    'Link': job_link
                })
                
                # Print first few extractions for debugging
                if i < 3:
                    print(f"   📋 Job {i+1}: {title} at {company}")
            
        except Exception as e:
            print(f"⚠️ Error extracting job {i+1}: {e}")
            continue
    
    print(f"✅ Successfully extracted {len(data)} jobs")
    return data

def save_data(data, filename_prefix="linkedin_jobs"):
    """Save data to CSV file"""
    if not data:
        print("❌ No data to save")
        return None
    
    df = pd.DataFrame(data)
    print(f"📊 DataFrame created with {len(df)} rows")
    
    # Remove duplicates based on job title and company
    df_cleaned = df.drop_duplicates(subset=['Job Title', 'Company'], keep='first')
    print(f"🧹 Removed {len(df) - len(df_cleaned)} duplicate entries")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    df_cleaned.to_csv(filename, index=False)
    print(f"💾 Saved {len(df_cleaned)} unique jobs to {filename}")
    return filename

def main():
    """Main scraping function"""
    print("🚀 Starting LinkedIn Job Scraper")
    print("="*50)
    
    driver = None
    try:
        # Create WebDriver
        driver = create_driver()
        print("✅ WebDriver created successfully")
        
        # Check login status
        driver.get("https://www.linkedin.com")
        time.sleep(3)
        
        if not check_and_wait_for_login(driver):
            print("❌ Login failed or timed out")
            return
        
        # Navigate to job search
        search_keywords = "Data Analyst"
        search_location = "New York City Metro Area"
        
        if not navigate_to_search(driver, search_keywords, search_location):
            print("❌ Failed to navigate to job search")
            return
        
        # Wait for initial content to load
        print("⏳ Waiting for initial content to load...")
        time.sleep(3)
        
        # Scroll to load more jobs
        if not scroll_job_results(driver, max_scrolls=6):
            print("❌ Scrolling failed")
            return
        
        # Extract job data
        print("🔍 Extracting job data...")
        job_data = extract_job_data(driver)
        
        if job_data:
            filename = save_data(job_data)
            if filename:
                print(f"🎉 Success! Scraped {len(job_data)} jobs and saved to {filename}")
            else:
                print("❌ Failed to save data")
        else:
            print("❌ No job data extracted - this might be due to LinkedIn's anti-bot measures")
            print("💡 Try these solutions:")
            print("   1. Solve any CAPTCHAs that appear in the browser")
            print("   2. Reduce the number of scrolls")
            print("   3. Wait a few minutes before trying again")
            print("   4. Manually interact with the browser to appear more human")
            
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Don't quit driver so you can see the browser state
        # driver.quit()
        print("\n🏁 Script completed. Check browser window for results.")
        print("💡 The browser window will remain open - you can close it manually when done.")

if __name__ == "__main__":
    main()