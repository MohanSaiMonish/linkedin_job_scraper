import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_driver():
    """Create and configure the Chrome WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--lang=en-US")
    
    # Adding these options to reduce chances of detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Execute CDP commands to mask automation
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            delete navigator.__proto__.webdriver;
            window.chrome = {runtime: {}};
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        '''
    })
    
    return driver

def test_page_loading(driver, url):
    """Test if the page loads correctly"""
    logger.info("Testing page loading...")
    try:
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        
        # Check page title
        title = driver.title
        logger.info(f"Page title: {title}")
        
        # Check if we're on LinkedIn
        if "LinkedIn" in title:
            logger.info("SUCCESS: Loaded LinkedIn page")
            return True
        else:
            logger.error("FAILED: Not on LinkedIn page")
            return False
    except Exception as e:
        logger.error(f"ERROR in page loading: {str(e)}")
        return False

def test_login_status(driver):
    """Check if we're logged in"""
    logger.info("Checking login status...")
    try:
        # Look for profile icon or sign in button
        sign_in_elements = driver.find_elements(By.XPATH, "//a[contains(text(), 'Sign in')]")
        profile_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'profile')]") 
        
        if len(sign_in_elements) > 0:
            logger.warning("NOT LOGGED IN: Found Sign in button")
            return False
        elif len(profile_elements) > 0:
            logger.info("LOGGED IN: Found profile elements")
            return True
        else:
            logger.info("UNCLEAR: Could not determine login status")
            return None
    except Exception as e:
        logger.error(f"ERROR checking login status: {str(e)}")
        return None

def test_search_navigation(driver, keywords="software engineer", location="United States"):
    """Test navigating to job search"""
    logger.info("Testing search navigation...")
    try:
        # Go to jobs page
        jobs_url = "https://www.linkedin.com/jobs/"
        driver.get(jobs_url)
        time.sleep(3)
        
        # Wait for search inputs
        wait = WebDriverWait(driver, 10)
        keyword_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword-id')]"))
        )
        
        location_input = driver.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-location-id')]")
        
        # Fill in search terms
        keyword_input.clear()
        keyword_input.send_keys(keywords)
        time.sleep(1)
        
        location_input.clear()
        location_input.send_keys(location)
        time.sleep(1)
        
        # Submit search
        search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
        search_button.click()
        time.sleep(5)
        
        logger.info("SUCCESS: Navigated to search results")
        return True
    except Exception as e:
        logger.error(f"ERROR in search navigation: {str(e)}")
        return False

def test_results_loading(driver):
    """Test if job results are loading"""
    logger.info("Testing results loading...")
    try:
        wait = WebDriverWait(driver, 10)
        # Wait for job results container
        results_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list"))
        )
        logger.info("SUCCESS: Found job results container")
        
        # Check initial job cards
        job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
        logger.info(f"Found {len(job_cards)} initial job cards")
        
        if len(job_cards) > 0:
            logger.info("SUCCESS: Job cards are visible")
            return True
        else:
            logger.warning("WARNING: No job cards found initially")
            return False
    except Exception as e:
        logger.error(f"ERROR in results loading: {str(e)}")
        return False

def test_scrolling(driver):
    """Test scrolling functionality"""
    logger.info("Testing scrolling...")
    try:
        # Get the results pane
        results_pane = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list"))
        )
        
        # Get initial scroll height
        initial_height = driver.execute_script("return arguments[0].scrollHeight", results_pane)
        logger.info(f"Initial scroll height: {initial_height}")
        
        # Perform scrolling
        scroll_pause_time = 2
        scroll_step = 5000
        current_position = 0
        
        for i in range(3):  # Test with 3 scrolls
            current_position += scroll_step
            driver.execute_script(f"arguments[0].scrollTop = {current_position}", results_pane)
            logger.info(f"Scrolled to position: {current_position}")
            time.sleep(scroll_pause_time)
            
            # Check new scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight", results_pane)
            logger.info(f"New scroll height: {new_height}")
            
            if new_height > initial_height:
                logger.info("SUCCESS: Content loaded after scrolling")
                return True
                
        logger.warning("WARNING: No new content loaded after scrolling")
        return False
    except Exception as e:
        logger.error(f"ERROR in scrolling: {str(e)}")
        return False

def test_data_extraction(driver):
    """Test extracting data from job cards"""
    logger.info("Testing data extraction...")
    try:
        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Look for job cards
        job_cards = soup.find_all('div', class_='job-card-container')
        logger.info(f"Found {len(job_cards)} job cards with BeautifulSoup")
        
        if len(job_cards) == 0:
            logger.warning("WARNING: No job cards found with BeautifulSoup")
            # Try alternative selectors
            job_cards = soup.find_all('a', class_='job-card-link')
            logger.info(f"Found {len(job_cards)} job card links with alternative selector")
            
        if len(job_cards) > 0:
            # Extract data from first card
            first_card = job_cards[0]
            logger.info("SUCCESS: Found job cards, attempting data extraction")
            
            # Try to extract title
            title_elem = first_card.find(['h3', 'h2', 'h4', 'span'], class_=lambda x: x and 'title' in x.lower()) or \
                         first_card.find(['h3', 'h2', 'h4']) or \
                         first_card.find('strong')
                         
            if title_elem:
                logger.info(f"SUCCESS: Extracted title: {title_elem.get_text(strip=True)[:50]}...")
            else:
                logger.warning("WARNING: Could not extract title from first card")
                
            return len(job_cards) > 0
        else:
            logger.error("FAILED: No job cards found for data extraction")
            return False
            
    except Exception as e:
        logger.error(f"ERROR in data extraction: {str(e)}")
        return False

def main():
    """Run all diagnostic tests"""
    driver = None
    try:
        logger.info("=== Starting LinkedIn Scraping Diagnostic ===")
        
        # Create driver
        driver = create_driver()
        logger.info("WebDriver created successfully")
        
        # Test 1: Page loading
        linkedin_url = "https://www.linkedin.com"
        if not test_page_loading(driver, linkedin_url):
            logger.error("Stopping diagnostic - page loading failed")
            return
            
        # Test 2: Login status
        login_status = test_login_status(driver)
        
        # Test 3: Search navigation
        if not test_search_navigation(driver):
            logger.error("Stopping diagnostic - search navigation failed")
            return
            
        # Test 4: Results loading
        if not test_results_loading(driver):
            logger.error("Stopping diagnostic - results loading failed")
            return
            
        # Test 5: Scrolling
        scroll_success = test_scrolling(driver)
        
        # Test 6: Data extraction
        extraction_success = test_data_extraction(driver)
        
        # Summary
        logger.info("=== Diagnostic Summary ===")
        logger.info(f"Login Status: {'Logged In' if login_status else 'Not Logged In' if login_status is False else 'Unknown'}")
        logger.info(f"Scrolling Test: {'PASS' if scroll_success else 'FAIL'}")
        logger.info(f"Data Extraction Test: {'PASS' if extraction_success else 'FAIL'}")
        
    except Exception as e:
        logger.error(f"Unexpected error in diagnostic: {str(e)}")
    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver closed")

if __name__ == "__main__":
    main()