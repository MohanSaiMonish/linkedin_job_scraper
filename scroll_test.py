from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

print("🔍 Scroll and Data Extraction Test")
print("=" * 40)

try:
    # Setup driver
    print("1. Setting up Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    print("   ✅ WebDriver setup complete")
    
    # Navigate to a test page with scrollable content
    print("2. Loading test page with scrollable content...")
    driver.get("https://quotes.toscrape.com/scroll")
    print(f"   Page loaded: {driver.title}")
    
    # Wait for content to load
    time.sleep(3)
    
    # Find scrollable container (body in this case)
    print("3. Finding scrollable container...")
    container = driver.find_element(By.TAG_NAME, "body")
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(f"   Initial height: {last_height}")
    
    # Scroll multiple times
    print("4. Performing scroll operations...")
    scrolls = 0
    max_scrolls = 3
    
    while scrolls < max_scrolls:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"   Scroll {scrolls + 1} completed")
        
        # Wait for new content to load
        time.sleep(2)
        
        # Check if new content loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"   New height: {new_height}")
        
        if new_height == last_height:
            print("   No new content loaded, stopping scroll")
            break
            
        last_height = new_height
        scrolls += 1
    
    # Extract data with BeautifulSoup
    print("5. Extracting data with BeautifulSoup...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find quotes
    quotes = soup.find_all('div', class_='quote')
    print(f"   Found {len(quotes)} quotes")
    
    # Display first few quotes
    for i, quote in enumerate(quotes[:3]):
        text = quote.find('span', class_='text')
        author = quote.find('small', class_='author')
        print(f"   Quote {i+1}: {text.text if text else 'N/A'} - {author.text if author else 'N/A'}")
    
    print("\n✅ Scroll and extraction test completed successfully!")
    print("   Browser will remain open for 20 seconds...")
    time.sleep(20)
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    import traceback
    traceback.print_exc()
    
print("🏁 Test finished")