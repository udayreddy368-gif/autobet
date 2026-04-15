from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# --- 1. Your proxy credentials (from your provider) ---
proxy_host = "your.proxy.provider.com"
proxy_port = 8080
proxy_user = "your_username"
proxy_pass = "your_password"

# --- 2. Configure seleniumwire_options ---
seleniumwire_options = {
    'proxy': {
        'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
        'https': f'https://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
        'no_proxy': 'localhost,127.0.0.1'  # Don't proxy local traffic
    }
}

# --- 3. Configure Chrome Options (like before) ---
chrome_options = {
    'headless': 'new',
    'no-sandbox': True,
    'disable-dev-shm-usage': True,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'disable-blink-features': 'AutomationControlled',
    'excludeSwitches': ['enable-automation'],
    'useAutomationExtension': False
}
options = Options()
for key, value in chrome_options.items():
    if isinstance(value, bool):
        if value:
            options.add_argument(f'--{key}')
    else:
        options.add_argument(f'--{key}={value}')

# --- 4. Launch with selenium-wire ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service,
    options=options,
    seleniumwire_options=seleniumwire_options
)

driver.get("https://zuplay.com/")
print(f"Page Title: {driver.title}")
driver.quit()