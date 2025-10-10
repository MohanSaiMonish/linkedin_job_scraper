from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_basic_browser():
    """Test if we can open a simple webpage"""
    try:
        # Define Chrome Options for basic testing
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) 
        chrome_options.add_argument("--window-size=1280,800")
        
        # Basic flags to reduce issues
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        print("Attempting to auto-install/load ChromeDriver...")
        
        # Use webdriver_manager to get the perfect Service instance
        S = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=S, options=chrome_options)
        driver.set_page_load_timeout(30)
        print("✅ WebDriver initialized successfully. Browser should be open.")
        
        # Try to load a simple website
        print("Attempting to load Google...")
        driver.get("https://www.google.com")
        print(f"Page loaded: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Wait a moment to see the page
        time.sleep(5)
        
        # Don't quit the driver to keep the browser open for inspection
        print("Test completed. Browser should remain open.")
        return True
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return False

if __name__ == "__main__":
    test_basic_browser()