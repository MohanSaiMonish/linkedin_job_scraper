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
from pathlib import Path
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager

print("🔍 Diagnostic LinkedIn Scraper")
print("=" * 40)

def diagnostic_step(step_name, func):
    """Helper function to run a step and report results"""
    print(f"\n🔧 {step_name}")
    try:
        result = func()
        print(f"   ✅ SUCCESS")
        return result, True
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def step1_setup_driver():
    """Step 1: Setup WebDriver"""
    global driver
    print("   Configuring Chrome options...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    print("   Installing/finding ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    
    print("   Creating WebDriver instance...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver

def step2_test_google():
    """Step 2: Test with Google"""
    print("   Navigating to Google...")
    driver.get("https://www.google.com")
    print(f"   Page title: {driver.title}")
    return driver.title

def step3_navigate_to_linkedin():
    """Step 3: Navigate to LinkedIn"""
    print("   Navigating to LinkedIn...")
    driver.get("https://www.linkedin.com")
    print(f"   Page title: {driver.title}")
    return driver.title

def step4_login_to_linkedin():
    """Step 4: Login to LinkedIn"""
    print("   Navigating to LinkedIn login...")
    driver.get("https://www.linkedin.com/login")
    print(f"   Page title: {driver.title}")
    
    # Wait for login elements
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    print("   ✅ Username field found")
    
    return driver.title

def step5_search_jobs():
    """Step 5: Search for jobs"""
    # For demo purposes, we'll use a simple job search URL
    keywords = "Data Analyst"
    location = "New York"
    keywords_encoded = keywords.replace(' ', '%20')
    location_encoded = location.replace(' ', '%20')
    jobs_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords_encoded}&location={location_encoded}"
    
    print(f"   Searching for jobs: {jobs_url}")
    driver.get(jobs_url)
    
    # Wait for job results
    wait = WebDriverWait(driver, 15)
    try:
        job_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
        print("   ✅ Job results container found")
        return True
    except TimeoutException:
        print("   ⚠️ Job results container not found, but continuing...")
        return False

def step6_scroll_jobs():
    """Step 6: Scroll job listings"""
    try:
        # Find the job results container
        job_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
        )
        print("   Found job results container")
        
        # Get initial height
        last_height = driver.execute_script("return arguments[0].scrollHeight;", job_container)
        print(f"   Initial scroll height: {last_height}")
        
        # Scroll a few times
        for i in range(3):
            print(f"   Scrolling... ({i+1}/3)")
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", job_container)
            time.sleep(2)
            
            # Check new height
            new_height = driver.execute_script("return arguments[0].scrollHeight;", job_container)
            print(f"   New scroll height: {new_height}")
            
            if new_height == last_height:
                print("   Reached end of scrollable content")
                break
                
            last_height = new_height
            
        return True
    except Exception as e:
        print(f"   Error during scrolling: {e}")
        return False

def step7_extract_data():
    """Step 7: Extract job data"""
    try:
        print("   Getting page source...")
        page_source = driver.page_source
        print(f"   Page source length: {len(page_source)} characters")
        
        print("   Parsing with BeautifulSoup...")
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Try to find job cards
        job_cards = soup.find_all('li', class_='jobs-search-results__list-item')
        print(f"   Found {len(job_cards)} job cards with primary selector")
        
        if len(job_cards) == 0:
            # Try alternative selectors
            job_cards = soup.find_all('div', {'data-job-id': True})
            print(f"   Found {len(job_cards)} job cards with data-job-id selector")
            
        if len(job_cards) == 0:
            # Try another selector
            job_cards = soup.find_all('a', class_='base-card__full-link')
            print(f"   Found {len(job_cards)} job cards with base-card selector")
            
        # Show some sample data
        if len(job_cards) > 0:
            print("   Sample job card content:")
            first_card = job_cards[0]
            print(f"     Card HTML preview: {str(first_card)[:200]}...")
            
        return len(job_cards)
    except Exception as e:
        print(f"   Error during data extraction: {e}")
        import traceback
        traceback.print_exc()
        return 0

def main():
    print("🚀 Starting Diagnostic LinkedIn Scraper")
    print("=" * 50)
    
    # Run diagnostic steps
    steps = [
        ("Setup WebDriver", step1_setup_driver),
        ("Test with Google", step2_test_google),
        ("Navigate to LinkedIn", step3_navigate_to_linkedin),
        ("Login to LinkedIn", step4_login_to_linkedin),
        ("Search for Jobs", step5_search_jobs),
        ("Scroll Job Listings", step6_scroll_jobs),
        ("Extract Job Data", step7_extract_data),
    ]
    
    results = []
    driver = None
    
    try:
        for step_name, step_func in steps:
            result, success = diagnostic_step(step_name, step_func)
            results.append((step_name, success, result))
            
            if not success and step_name not in ["Search for Jobs"]:
                print(f"\n💥 Stopping diagnostic at failed step: {step_name}")
                break
                
            time.sleep(1)  # Brief pause between steps
    
        # Summary
        print(f"\n📊 Diagnostic Summary")
        print("=" * 30)
        passed = sum(1 for _, success, _ in results if success)
        total = len(results)
        
        for step_name, success, _ in results:
            status = "✅" if success else "❌"
            print(f"{status} {step_name}")
            
        print(f"\n📈 Results: {passed}/{total} steps passed")
        
        if passed == total:
            print("🎉 All diagnostic steps passed!")
        elif passed >= total * 0.8:
            print("⚠️ Most steps passed, minor issues detected")
        else:
            print("❌ Critical issues detected")
            
    except KeyboardInterrupt:
        print("\n⚠️ Diagnostic interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🏁 Diagnostic completed")
        print("   Browser will remain open for 30 seconds...")
        time.sleep(30)

if __name__ == "__main__":
    main()