from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

def extract_item_data(item):
    try:
        name = item.find_element(By.CSS_SELECTOR, "h3.clsgetname").text
        
        try:
            final_price = item.find_element(By.CSS_SELECTOR, "span.final-price").text
        except:
            final_price = item.find_element(By.CSS_SELECTOR, "span#final_price").text
        
        try:
            mrp = item.find_element(By.CSS_SELECTOR, "strike").text
        except:
            mrp = final_price
            
        return {
            "name": name,
            "final_price": final_price,
            "mrp": mrp
        }
    except Exception as e:
        print(f"Error extracting item: {e}")
        return None

if __name__ == "__main__":
    url = "https://www.netmeds.com/non-prescriptions/ayush"
    driver = init_driver()
    driver.get(url)
    scroll_page(driver)

    items = driver.find_elements(By.CSS_SELECTOR, "div.cat-item")
    results = []

    for item in items:
        data = extract_item_data(item)
        if data:
            results.append(data)

    driver.quit()

    for r in results:
        print(r)
