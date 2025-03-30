from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def init_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scroll_page(driver, max_attempts=150, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    
    while attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            attempts += 1
        else:
            attempts = 0
        last_height = new_height

if __name__ == "__main__":
    url = "https://www.netmeds.com/non-prescriptions/ayush"
    driver = init_driver()
    driver.get(url)
    scroll_page(driver)
    driver.quit()