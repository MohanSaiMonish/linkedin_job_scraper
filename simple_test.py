from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

print("🔧 Simple Browser Test")
print("=" * 30)

try:
    print("1. Configuring Chrome options...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    print("2. Installing/finding ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    
    print("3. Creating WebDriver instance...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("4. Setting page load timeout...")
    driver.set_page_load_timeout(30)
    
    print("5. Navigating to Google...")
    driver.get("https://www.google.com")
    
    print(f"6. Page title: {driver.title}")
    print(f"7. Current URL: {driver.current_url}")
    
    print("✅ Test completed successfully!")
    print("   Browser should remain open for 10 seconds...")
    
    time.sleep(10)
    print("✅ Script finished.")
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    import traceback
    traceback.print_exc()