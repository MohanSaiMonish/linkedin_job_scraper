import time
import sys

print("🔍 Debug Test - Step by Step")
print("=" * 40)

# Import statements with error handling
try:
    print("1. Importing Selenium modules...")
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    print("   ✅ Selenium modules imported")
except Exception as e:
    print(f"   ❌ Selenium import failed: {e}")
    sys.exit(1)

try:
    print("2. Importing WebDriverManager...")
    from webdriver_manager.chrome import ChromeDriverManager
    print("   ✅ WebDriverManager imported")
except Exception as e:
    print(f"   ❌ WebDriverManager import failed: {e}")
    sys.exit(1)

try:
    print("3. Configuring Chrome options...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    print("   ✅ Chrome options configured")
except Exception as e:
    print(f"   ❌ Chrome options configuration failed: {e}")
    sys.exit(1)

try:
    print("4. Installing/finding ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    print("   ✅ ChromeDriver installed/found")
except Exception as e:
    print(f"   ❌ ChromeDriver installation failed: {e}")
    sys.exit(1)

try:
    print("5. Creating WebDriver instance...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("   ✅ WebDriver instance created")
except Exception as e:
    print(f"   ❌ WebDriver creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("6. Setting page load timeout...")
    driver.set_page_load_timeout(45)
    print("   ✅ Page load timeout set")
except Exception as e:
    print(f"   ❌ Setting page load timeout failed: {e}")

try:
    print("7. Navigating to Google (control test)...")
    driver.get("https://www.google.com")
    print(f"   ✅ Google loaded: {driver.title}")
    print(f"   URL: {driver.current_url}")
except Exception as e:
    print(f"   ❌ Google loading failed: {e}")
    import traceback
    traceback.print_exc()

print("8. Waiting 3 seconds...")
time.sleep(3)

try:
    print("9. Navigating to a simple test page...")
    driver.get("https://httpbin.org/html")
    print(f"   ✅ Test page loaded: {driver.title}")
    print(f"   URL: {driver.current_url}")
except Exception as e:
    print(f"   ❌ Test page loading failed: {e}")
    import traceback
    traceback.print_exc()

print("10. Waiting 3 seconds...")
time.sleep(3)

try:
    print("11. Navigating to LinkedIn...")
    driver.get("https://www.linkedin.com")
    print(f"   ✅ LinkedIn loaded: {driver.title}")
    print(f"   URL: {driver.current_url}")
except Exception as e:
    print(f"   ❌ LinkedIn loading failed: {e}")
    import traceback
    traceback.print_exc()

print("12. Waiting 3 seconds...")
time.sleep(3)

try:
    print("13. Navigating to LinkedIn login...")
    driver.get("https://www.linkedin.com/login")
    print(f"   ✅ LinkedIn login loaded: {driver.title}")
    print(f"   URL: {driver.current_url}")
except Exception as e:
    print(f"   ❌ LinkedIn login loading failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Debug test completed!")
print("   Browser will remain open for 30 seconds...")
time.sleep(30)
print("🏁 Script finished.")