from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

options = Options()

# Headless mode with better camouflage
options.add_argument("--headless=new")          # Newer headless mode (less detectable)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

# Spoof a common user agent
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

# Additional evasion flags
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-features=IsolateOrigins,site-per-process")
options.add_argument("--disable-site-isolation-trials")

# Exclude automation switches
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Launch browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Execute CDP command to hide webdriver property
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
    """
})

# Navigate to site
driver.get("https://zuplay.com/")
time.sleep(3)  # Allow redirects/JS to settle
print("Page title:", driver.title)
print("Current URL:", driver.current_url)

driver.quit()