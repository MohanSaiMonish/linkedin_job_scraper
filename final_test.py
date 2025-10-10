from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

print("🔬 Final Comprehensive Test")
print("=" * 40)

# Test results tracking
test_results = []

def log_result(test_name, success, details=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"   {status} {test_name} {details}")
    test_results.append((test_name, success, details))

try:
    print("1. Setting up Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-timer-throttling")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    log_result("WebDriver Setup", True)
    
except Exception as e:
    log_result("WebDriver Setup", False, str(e))
    print("❌ Critical failure in WebDriver setup. Exiting.")
    exit(1)

# Test different websites
websites = [
    ("Google", "https://www.google.com"),
    ("HTTPBin", "https://httpbin.org/html"),
    ("LinkedIn Home", "https://www.linkedin.com"),
    ("LinkedIn Login", "https://www.linkedin.com/login")
]

for name, url in websites:
    print(f"2. Testing {name} ({url})...")
    try:
        start_time = time.time()
        driver.get(url)
        load_time = time.time() - start_time
        
        title = driver.title
        current_url = driver.current_url
        
        # Check if it's a blank page
        if not title or title.strip() == "":
            log_result(f"{name} Load", False, f"Blank title, URL: {current_url}")
        else:
            log_result(f"{name} Load", True, f"Title: '{title}', Load time: {load_time:.2f}s")
            
    except Exception as e:
        log_result(f"{name} Load", False, str(e))
    
    time.sleep(2)

# Test finding elements on LinkedIn login page
if any(name == "LinkedIn Login" and success for name, success, _ in test_results):
    print("3. Testing element detection on LinkedIn login...")
    try:
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        log_result("Element Detection", True, "Found username and password fields")
    except Exception as e:
        log_result("Element Detection", False, str(e))
else:
    print("3. Skipping element detection (LinkedIn login not loaded)")
    log_result("Element Detection", False, "Skipped - LinkedIn login not loaded")

# Summary
print("\n📊 Test Summary")
print("=" * 40)
passed = sum(1 for _, success, _ in test_results if success)
total = len(test_results)

for name, success, details in test_results:
    status = "✅" if success else "❌"
    print(f"{status} {name}: {details}")

print(f"\n📈 Results: {passed}/{total} tests passed")

if passed == total:
    print("🎉 All tests passed! The scraper should work correctly.")
else:
    print("⚠️ Some tests failed. Check the results above for details.")
    
print("\n💡 Keeping browser open for 30 seconds...")
time.sleep(30)
print("🏁 Test completed.")