﻿from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import getpass
import sys # To exit the script on failure
import os
from pathlib import Path
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager  # fallback installer

# --- Configuration ---
PROJECT_DIR = Path(__file__).parent
load_dotenv(PROJECT_DIR / ".env")
# Driver path resolution: prefer env var CHROME_DRIVER_PATH, otherwise OS-specific default
_env_driver_path = os.getenv("CHROME_DRIVER_PATH", "").strip()
if _env_driver_path:
    CHROME_DRIVER_PATH = _env_driver_path
else:
    # Default to Windows exe if running on Windows; else unix filename
    CHROME_DRIVER_PATH = './chromedriver.exe' if os.name == 'nt' else './chromedriver'

# --- Core Functions ---

def prompt_linkedin_credentials():
    """Fetches credentials from env vars or prompts securely if missing."""
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    if email and password:
        return email, password
    try:
        email = input("Enter your LinkedIn email: ") if not email else email
        password = getpass.getpass("Enter your LinkedIn password: ") if not password else password
        return email, password
    except Exception as e:
        print(f"Error getting input: {e}")
        return None, None

def linkedin_login(driver, email, password):
    """Navigates to LinkedIn login and attempts to sign in."""
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 15)

    try:
        # 1. Fill Username
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(email)

        # 2. Fill Password
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)

        # 3. Click Login Button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']")))
        login_button.click()

        print("Login attempt initiated...")

        # 4. Wait for successful post-login element (e.g., the global search bar)
        wait.until(EC.presence_of_element_located((By.ID, "global-nav-typeahead")))
        print("✅ Successfully logged into LinkedIn.")
        return True

    except Exception as e:
        print(f"❌ Login failed! Check credentials or selectors. Error: {e}")
        return False

def navigate_to_jobs(driver, keywords, location):
    """Constructs the job search URL and navigates the browser."""
    
    # Simple URL encoding (replacing spaces with %20)
    keywords_encoded = keywords.replace(' ', '%20')
    location_encoded = location.replace(' ', '%20')

    # Construct the search URL
    jobs_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords_encoded}&location={location_encoded}"

    driver.get(jobs_url)
    wait = WebDriverWait(driver, 15)
    
    # Wait for the main job results container to ensure the page is loaded
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
        print(f"✅ Job search results page loaded for '{keywords}' in '{location}'.")
        return jobs_url
    except Exception as e:
        print(f"❌ Failed to load job search results page: {e}")
        return None

# --- Main Execution Block ---

if __name__ == "__main__":
    
    # --- 1. WebDriver Setup ---
    try:
        # Prepare visible (non-headless) Chrome options and keep window open after script ends
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--window-size=1280,800")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--dns-prefetch-disable")
        # Make browser look less automated
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # type: ignore[arg-type]
        chrome_options.add_experimental_option("useAutomationExtension", False)  # type: ignore[arg-type]
        chrome_options.add_argument("--lang=en-US,en;q=0.9")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Try local chromedriver first
        S = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=S, options=chrome_options)
        driver.set_page_load_timeout(30)
        # CDP tweaks to reduce detection
        try:
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
        except Exception:
            pass
        print("WebDriver initialized (local driver). Browser window should be visible.")
    except Exception as e:
        print(f"Local driver failed: {e}")
        print("Falling back to webdriver-manager to auto-install the correct ChromeDriver...")
        try:
            S = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=S, options=chrome_options)
            driver.set_page_load_timeout(30)
            try:
                driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                })
            except Exception:
                pass
            print("WebDriver initialized (webdriver-manager). Browser window should be visible.")
        except Exception as ee:
            print("Error setting up WebDriver. Verify Chrome is installed and accessible.")
            print(f"Error details: {ee}")
            sys.exit(1)

    # --- 2. Interactive/Login via env and Navigation ---
    
    email, password = prompt_linkedin_credentials()
    if email is None or password is None:
        driver.quit()
        sys.exit(1)

    # Ensure we can reach LinkedIn before attempting login
    try:
        driver.get("https://www.linkedin.com/login")
    except TimeoutException:
        print("Page load timed out. Retrying once...")
        try:
            driver.get("https://www.linkedin.com/login")
        except Exception as e:
            print(f"Failed to load LinkedIn login: {e}")
            driver.quit()
            sys.exit(1)

    if linkedin_login(driver, email, password):
        # The two lines you requested to add:
        url = navigate_to_jobs(driver, keywords="Data Analyst", location="New York City Metro Area")
        print("Navigating to:", url)
        
        # Keep the browser open for 15 seconds to visually confirm the page loaded
        time.sleep(15)

    # --- 3. Cleanup ---
    driver.quit()
    print("Browser closed. Script finished.")