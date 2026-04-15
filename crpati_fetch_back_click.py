from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

# Headless Chrome setup for Codespaces
chrome_options = Options()
chrome_options.add_argument("--headless")               # Use standard headless (not --headless=new)
chrome_options.add_argument("--no-sandbox")             # Required in container
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents /dev/shm overflow
chrome_options.add_argument("--disable-gpu")            # No GPU in Codespaces
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ensure prerequisites are installed
# pip install selenium beautifulsoup4

# Path to your chromedriver
# driver_path = r'C:\Users\USER\Desktop\crpati\chromedriver.exe'  # Update this path
# Create a Service object
# service = Service(driver_path)

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

chrome_options = Options()
chrome_options.add_argument("--headless=new")          # Run without GUI
chrome_options.add_argument("--no-sandbox")            # Required for Codespaces
chrome_options.add_argument("--disable-dev-shm-usage") # Avoid memory issues
chrome_options.add_argument("--disable-gpu")           # Disable GPU acceleration

# Automatically download and manage ChromeDriver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create ChromeOptions object to configure the browser
chrome_options = Options()

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to open
url = 'https://zuplay.com/'

# Open the URL
driver.get(url)

# After opening the URL and closing popup, automate login:
username_field = driver.find_element(By.ID, "username")   # Update selectors
password_field = driver.find_element(By.ID, "password")
username_field.send_keys("UdayReddy347")
password_field.send_keys("Uday@11347")
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Handle the popup if it appears
try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@class='dark-close' and @type='button']"))
    )
    close_button = driver.find_element(By.XPATH, "//button[@class='dark-close' and @type='button']")
    close_button.click()
    print("Popup closed successfully!")
except Exception as e:
    print(f"No popup appeared: {e}")

# Wait for and click the login button
try:
    login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='signin' and @title='Log In']"))
    )
    # Scroll into view to avoid interception
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    time.sleep(1)  # Allow time for any animation to complete
    # Use JavaScript click to bypass interception
    driver.execute_script("arguments[0].click();", login_button)
    print("Login button clicked successfully!")
except Exception as e:
    print(f"Error interacting with the login button: {str(e)}")

# Allow manual login
input("Please log in manually. Press Enter when done...")

# Wait for the user to open a new tab and navigate to the match
input("Open the desired page in a new tab. Press Enter when done...")

# Get all open tabs (window handles) and switch to the last one
all_windows = driver.window_handles
if len(all_windows) > 1:
    driver.switch_to.window(all_windows[-1])
    print(f"Switched to the new tab: {driver.current_url}")
else:
    print("No new tab detected. Exiting...")
    driver.quit()
    exit()

# Allow user to select the live match manually
input("Select the live match manually. Press Enter when done...")

# Capture the match URL and navigate to it
match_url = driver.current_url
print(f"Captured match URL: {match_url}")

# Ensure the page is fully loaded
driver.get(match_url)
time.sleep(5)  # Increased time to wait for dynamic content to load

# Freeze rendering
try:
    driver.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": True})
    print("Rendering paused successfully.")
except Exception as e:
    print(f"Error pausing rendering: {e}")

# Wait until the element is completely visible and has been populated
try:
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//td[@id='back_1' and @fullmarketodds]"))
    )

    # Parse the page source using Beautiful Soup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    print("Page source successfully parsed with Beautiful Soup.")

    # Locate the back <td> element using Beautiful Soup
    td_back = soup.find('td', {'id': 'back_1', 'fullmarketodds': True})
    if td_back:
        print(f"HTML of <td> element for back odds: {td_back}")

        # Find the <a> element inside the <td> for back odds
        a_back = td_back.find('a')
        if a_back:
            odds_back = ''.join(a_back.find_all(string=True, recursive=False)).strip()
            print(f"Extracted back value: {odds_back}")
        else:
            print("No <a> element found inside back <td>.")
    else:
        print("No matching <td> element for back odds.")

    # **Added Block: Locate the lay <td> element using Beautiful Soup**
    td_lay = soup.find('td', {'class': 'spark', 'fullmarketodds': True})
    if td_lay:
        print(f"HTML of <td> element for lay odds: {td_lay}")

        # Find the <a> element inside the <td> for lay odds
        a_lay = td_lay.find('a')
        if a_lay:
            odds_lay = ''.join(a_lay.find_all(string=True, recursive=False)).strip()
            print(f"Extracted lay value: {odds_lay}")
        else:
            print("No <a> element found inside lay <td>.")
    else:
        print("No matching <td> element for lay odds.")

except Exception as e:
    print(f"Error fetching or waiting for the <td> element: {str(e)}")

# Resume rendering after capturing the element
try:
    driver.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": False})
    print("Rendering resumed successfully.")

    # **New Block: Click on the <td> element if odds_back is greater than 1**
    if float(odds_back) > 1:
        td_to_click = driver.find_element(By.XPATH, "//td[@id='back_1' and @class='back-1 select spark']")
        td_to_click.click()
        print("Clicked on the <td> element with odds greater than 1.")
        time.sleep(20)  # Wait for 20 seconds after clicking
except Exception as e:
    print(f"Error resuming rendering: {e}")

# Keep the browser open until you manually close it
input("Press Enter to close the browser...")

# Close the browser when done
driver.quit()
