from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def create_driver():
    """Create and configure the Chrome WebDriver"""
    chrome_options = Options()
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
    return driver

def check_login_status(driver):
    """Check if we're logged into LinkedIn"""
    print("Checking login status...")
    
    # Go to LinkedIn homepage
    driver.get("https://www.linkedin.com")
    time.sleep(3)
    
    # Check for profile elements (indicates logged in)
    profile_elements = driver.find_elements(By.CSS_SELECTOR, "img.global-nav__profile-photo, img.nav-item__profile-member-photo")
    
    # Check for sign in button (indicates not logged in)
    sign_in_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/login') and contains(text(), 'Sign in')]")
    
    print(f"Page title: {driver.title}")
    
    if profile_elements:
        print("✅ You are logged into LinkedIn")
        # Get profile name if available
        try:
            profile_name = driver.find_element(By.CSS_SELECTOR, ".global-nav__me-photo.lazy-image.ember-view")
            print(f"Profile detected")
        except:
            pass
        return True
    elif sign_in_elements:
        print("❌ You are NOT logged into LinkedIn")
        print("Please log in manually in the browser window, then run the scraper again")
        return False
    else:
        print("? Login status unclear - you may need to log in manually")
        return None

def main():
    driver = None
    try:
        driver = create_driver()
        login_status = check_login_status(driver)
        
        if login_status:
            print("\n✅ Ready to scrape - you're logged in")
        elif login_status is False:
            print("\n❌ Please log in to LinkedIn in the browser window that opened")
            print("After logging in, run the scraper script again")
            # Keep browser open for manual login
            input("Press Enter after you've logged in manually...")
        else:
            print("\n? Unclear login status - check the browser window")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if driver:
            # Don't quit so user can see the browser
            # driver.quit()
            pass

if __name__ == "__main__":
    main()