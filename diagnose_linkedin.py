from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def diagnose_linkedin_access():
    """Diagnose LinkedIn access issues"""
    try:
        # Define Chrome Options with aggressive anti-detection
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) 
        chrome_options.add_argument("--window-size=1280,800")
        
        # Anti-detection flags
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Stability flags
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # User Agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        print("Attempting to auto-install/load ChromeDriver...")
        
        # Use webdriver_manager to get the perfect Service instance
        S = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=S, options=chrome_options)
        driver.set_page_load_timeout(45)
        print("✅ WebDriver initialized successfully. Browser should be open.")
        
        # Apply CDP tweak
        try:
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
            print("✅ CDP script executed successfully.")
        except Exception as e:
            print(f"⚠️ CDP script failed: {e}")
        
        # Try to load LinkedIn
        print("Attempting to load LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Check if we're on the actual LinkedIn page or a blocked page
        if "linkedin" in driver.current_url.lower():
            print("✅ Successfully loaded LinkedIn login page!")
        else:
            print("❌ Did not load LinkedIn. Current page may be a block page.")
            
        # Wait to observe the page
        time.sleep(10)
        
        print("Diagnostic completed. Browser should remain open for inspection.")
        return True
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return False

if __name__ == "__main__":
    diagnose_linkedin_access()