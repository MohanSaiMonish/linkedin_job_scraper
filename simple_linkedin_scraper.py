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

def create_driver():
    """Create and configure the Chrome WebDriver"""
    chrome_options = Options()
    # Remove headless option so you can see what's happening
    chrome_options.add_experimental_option("detach", True)  # Keep window open after script ends
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

    print("Installing/finding ChromeDriver...")
    
    # Auto-install ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(45)
    
    # Execute CDP commands to mask automation
    try:
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
    except Exception as e:
        print(f"Warning: Could not execute CDP command: {e}")
    
    return driver

def navigate_to_search(driver, keywords="Data Analyst", location="New York City Metro Area"):
    """Navigate directly to job search results"""
    # URL encode search terms
    keywords_encoded = keywords.replace(' ', '%20')
    location_encoded = location.replace(' ', '%20')
    
    # Direct URL to job search
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords_encoded}&location={location_encoded}"
    
    print(f"Navigating to: {search_url}")
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
        # Print page title to see what page we're actually on
        print(f"Current page title: {driver.title}")
        return False

def scroll_job_results(driver, max_scrolls=5):
    """Scroll through job results to load more listings"""
    print("🔍 Starting scroll operations...")
    
    try:
        # Find the scrollable results pane
        results_pane = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list"))
        )
        
        # Get initial scroll height
        last_height = driver.execute_script("return arguments[0].scrollHeight", results_pane)
        print(f"Initial scroll height: {last_height}")
        
        scroll_count = 0
        while scroll_count < max_scrolls:
            # Scroll to bottom of results pane
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_pane)
            print(f"Scroll #{scroll_count + 1} completed")
            
            # Wait for new content to load
            time.sleep(3)
            
            # Check new scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight", results_pane)
            print(f"New scroll height: {new_height}")
            
            # If height didn't change, we've reached the end
            if new_height == last_height:
                print("Reached end of job listings")
                break
                
            last_height = new_height
            scroll_count += 1
            
        print(f"✅ Completed {scroll_count} scroll operations")
        return True
        
    except Exception as e:
        print(f"❌ Error during scrolling: {e}")
        return False

def extract_job_data(driver):
    """Extract job data using BeautifulSoup"""
    print("🔍 Extracting job data...")
    
    # Get page source after scrolling
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Try multiple selectors for job cards
    job_cards = []
    
    # Selector 1: Main job card container
    cards = soup.find_all('div', class_='job-card-container')
    if cards:
        job_cards.extend(cards)
        print(f"Found {len(cards)} job cards with 'job-card-container'")
    
    # Selector 2: List item approach
    if not job_cards:
        cards = soup.find_all('li', class_='jobs-search-results__list-item')
        if cards:
            job_cards.extend(cards)
            print(f"Found {len(cards)} job cards with 'jobs-search-results__list-item'")
    
    # Selector 3: Data attribute approach
    if not job_cards:
        cards = soup.find_all('div', {'data-job-id': True})
        if cards:
            job_cards.extend(cards)
            print(f"Found {len(cards)} job cards with 'data-job-id'")
    
    print(f"Total job cards found: {len(job_cards)}")
    
    if not job_cards:
        # Print a portion of the page source for debugging
        print("No job cards found. Printing first 1000 chars of page source:")
        print(driver.page_source[:1000])
        return []
    
    data = []
    for i, card in enumerate(job_cards[:10]):  # Limit to first 10 for testing
        try:
            # Extract job title
            title_elem = card.find('a', class_='job-card-list__title') or \
                        card.find('h3', class_='base-search-card__title') or \
                        card.find('span', class_='sr-only')
            
            # Extract company name
            company_elem = card.find('a', class_='job-card-container__company-name') or \
                          card.find('h4', class_='base-search-card__subtitle') or \
                          card.find('a', class_='hidden-nested-link')
            
            # Extract location
            location_elem = card.find('span', class_='job-card-container__metadata-item') or \
                           card.find('span', class_='job-search-card__location') or \
                           card.find('li', class_='job-card-container__metadata-item')
            
            # Extract post date
            date_elem = card.find('time')
            
            # Extract job link
            link_elem = card.find('a', class_='job-card-list__title') or \
                       card.find('a', class_='base-card__full-link')
            
            # Get text content
            title = title_elem.get_text(strip=True) if title_elem else 'N/A'
            company = company_elem.get_text(strip=True) if company_elem else 'N/A'
            location = location_elem.get_text(strip=True) if location_elem else 'N/A'
            post_date = date_elem.get('datetime', '') if date_elem else 'N/A'
            job_link = link_elem.get('href', 'N/A') if link_elem else 'N/A'
            
            # Clean up link
            if job_link != 'N/A':
                job_link = job_link.split('?')[0] if '?' in job_link else job_link
            
            data.append({
                'Job Title': title,
                'Company': company,
                'Location': location,
                'Post Date': post_date,
                'Link': job_link
            })
            
            print(f"Extracted job {i+1}: {title} at {company}")
            
        except Exception as e:
            print(f"Error extracting job {i+1}: {e}")
            continue
    
    return data

def save_data(data, filename_prefix="linkedin_jobs"):
    """Save data to CSV file"""
    if not data:
        print("No data to save")
        return
    
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(data)} jobs to {filename}")

def main():
    """Main scraping function"""
    print("🚀 Starting LinkedIn Job Scraper")
    
    driver = None
    try:
        # Create WebDriver
        driver = create_driver()
        print("✅ WebDriver created successfully")
        
        # Navigate to job search
        if not navigate_to_search(driver):
            print("❌ Failed to navigate to job search")
            return
        
        # Wait a bit for initial content to load
        time.sleep(3)
        
        # Scroll to load more jobs
        if not scroll_job_results(driver):
            print("❌ Scrolling failed")
            return
        
        # Extract job data
        job_data = extract_job_data(driver)
        
        if job_data:
            print(f"✅ Successfully extracted {len(job_data)} jobs")
            save_data(job_data)
        else:
            print("❌ No job data extracted")
            
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Don't quit driver so you can see the browser state
        # driver.quit()
        print("🏁 Script completed. Check browser window for results.")

if __name__ == "__main__":
    main()