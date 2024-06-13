from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests

# Specify the path to the ChromeDriver
chromedriver_path = '/Users/anton/python/chromedriver'

# Telegram bot credentials
bot_token = 'token'
chat_id = 'chatid'

# Function to send message to Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        print("Telegram message sent successfully")
    except requests.exceptions.HTTPError as e:
        print(f"Error sending Telegram message: {e}")

# Create a Service object with the path to the ChromeDriver
service = Service(chromedriver_path)

# Set up Chrome options to run in headless mode
options = Options()
options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration (optional)
options.add_argument('--no-sandbox')   # Bypass OS security model (useful for Linux)
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems (optional)

# Initialize the Chrome WebDriver with the service object and options
driver = webdriver.Chrome(service=service, options=options)
# Set a maximum load time of 30 seconds
driver.set_page_load_timeout(30)

# Function to check if the page returns status code 200
def check_status_code(url):
    try:
        response = requests.get(url)
        print("Stats code of " + url +" is: " + str(response.status_code))
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error checking status code for {url}: {e}")
        return False

# Function to measure page load time
def measure_load_time(url):
    start_time = time.time()
    try:
        driver.get(url)
        end_time = time.time()
        load_time = end_time - start_time
        return load_time
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return None

# URLs to check
urls = ["http://bloomex.ca", "http://bloomex.com.au", "http://thingsengraved.ca"]

# Load time threshold in seconds
threshold = 10

# Measure and print load times for each URL
for url in urls:
    if check_status_code(url):
        load_time = measure_load_time(url)
        if load_time is None:
            message = f"⚠️ ALERT: Page {url} did not load within 30 seconds."
            # Send alert to Telegram
            send_telegram_message(bot_token, chat_id, message)
            print(f"Page {url} did not load within 30 seconds.")
        elif load_time > threshold:
            message = f"⚠️ ALERT: Page load time for {url} exceeded threshold ({threshold} seconds).\nLoad time: {load_time:.2f} seconds"
            # Send alert to Telegram
            send_telegram_message(bot_token, chat_id, message)
            print(f"Page load time for {url}: {load_time:.2f} seconds (exceeded threshold)")
        else:
            print(f"Page load time for {url}: {load_time:.2f} seconds (within threshold)")
    else:
        message = f"⚠️ ALERT: Page {url} returned a status code other than 200."
        # Send alert to Telegram
        send_telegram_message(bot_token, chat_id, message)
        print(f"Page {url} returned a status code other than 200.")

# Close the browser
driver.quit()

