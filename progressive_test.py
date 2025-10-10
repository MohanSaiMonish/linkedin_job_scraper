from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_step(step_name, func):
    """Helper function to run a test step and report results"""
    print(f"\n🔍 {step_name}")
    try:
        result = func()
        print(f"   ✅ {step_name} - SUCCESS")
        return result, True
    except Exception as e:
        print(f"   ❌ {step_name} - FAILED: {e}")
        return None, False

def step1_basic_driver():
    """Step 1: Create basic driver"""
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver

def step2_load_google():
    """Step 2: Load Google"""
    driver.get("https://www.google.com")
    return driver.title

def step3_load_linkedin():
    """Step 3: Load LinkedIn"""
    driver.get("https://www.linkedin.com")
    return driver.title

def step4_load_linkedin_login():
    """Step 4: Load LinkedIn login page"""
    driver.get("https://www.linkedin.com/login")
    return driver.title

def step5_find_login_elements():
    """Step 5: Find login elements"""
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    return f"Found username and password fields"

def main():
    print("🧪 Progressive LinkedIn Scraper Test")
    print("=" * 50)
    
    # Run tests progressively
    driver = None
    steps = [
        ("Create WebDriver", step1_basic_driver),
        ("Load Google", step2_load_google),
        ("Load LinkedIn Home", step3_load_linkedin),
        ("Load LinkedIn Login", step4_load_linkedin_login),
        ("Find Login Elements", step5_find_login_elements),
    ]
    
    for step_name, step_func in steps:
        result, success = test_step(step_name, step_func)
        if not success:
            print(f"\n💥 Test stopped at step: {step_name}")
            if driver:
                print("   Keeping browser open for inspection...")
                time.sleep(30)
            return
        time.sleep(2)  # Brief pause between steps
    
    print(f"\n🎉 All tests passed!")
    print("   Keeping browser open for 30 seconds...")
    time.sleep(30)
    print("✅ Test sequence completed.")

if __name__ == "__main__":
    main()