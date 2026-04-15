from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options   # ← Import was missing
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Proxy configuration (example using a free proxy) ---
# Replace with a working proxy IP:PORT from a free proxy list
proxy_ip = "138.68.60.8"
proxy_port = "3128"

seleniumwire_options = {
    'proxy': {
            'http': f'http://{proxy_ip}:{proxy_port}',
                    'https': f'https://{proxy_ip}:{proxy_port}',
                            'no_proxy': 'localhost,127.0.0.1'
                                }
                                }

# --- Chrome options (headless + anti-detection) ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# --- Launch browser ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service,
    options=options,
    seleniumwire_options=seleniumwire_options
)

# Hide WebDriver property
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
})

# Test the connection
driver.get("https://zuplay.com/")
print("Page title:", driver.title)
print("Current URL:", driver.current_url)

driver.quit()