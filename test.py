from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Your proxy (IP:PORT)
proxy = "45.140.147.82:1081"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f'--proxy-server=http://{proxy}')   # ← Direct proxy

# ... rest of your anti-detection options ...

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://zuplay.com/")
print(driver.title)
driver.quit()