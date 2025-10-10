from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

print("🔍 Detailed Diagnostic Test")
print("=" * 40)

try:
    print("1. Configuring Chrome options...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    
    print("2. Installing/finding ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    
    print("3. Creating WebDriver instance...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("4. Setting page load timeout...")
    driver.set_page_load_timeout(30)
    
    print("5. Navigating to Google (control test)...")
    driver.get("https://www.google.com")
    print(f"   ✅ Google loaded: {driver.title}")
    
    print("6. Waiting 5 seconds...")
    time.sleep(5)
    
    print("7. Navigating to LinkedIn...")
    driver.get("https://www.linkedin.com")
    print(f"   ✅ LinkedIn loaded: {driver.title}")
    print(f"   URL: {driver.current_url}")
    
    print("8. Waiting 5 seconds...")
    time.sleep(5)
    
    print("9. Navigating to LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")
    print(f"   ✅ LinkedIn login loaded: {driver.title}")
    print(f"   URL: {driver.current_url}")
    
    print("\n✅ All tests completed successfully!")
    print("   Browser will remain open for 30 seconds...")
    time.sleep(30)
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    import traceback
    print("🔍 Full traceback:")
    traceback.print_exc()
    
    print("\n💡 Troubleshooting suggestions:")
    print("   1. Check your internet connection")
    print("   2. Try temporarily disabling antivirus/firewall")
    print("   3. Make sure Chrome is updated to the latest version")
    print("   4. Try running the script as administrator")
    
    # Keep the script alive for a moment to see the error
    time.sleep(10)

print("🏁 Diagnostic test finished.")