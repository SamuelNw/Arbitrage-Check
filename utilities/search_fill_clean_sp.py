from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import time

HOME_PAGE_URL = "https://www.ke.sportpesa.com/sports/football?sportId=1&section=highlights"
SEARCH_PAGE_STATIC_URL = "https://www.ke.sportpesa.com/search?sportId=1&text="
COOKIES_ACCEPT_DIV = "cookies-law-info-content"

driver_path = "/Users/sam/Desktop/Cipher/Ciphy/Arbitrage-Check/drivers/chromedriver"

def initialize_driver():
    service = Service(executable_path=driver_path)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    return webdriver.Chrome(service=service, options=chrome_options)

def safe_get(driver, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver.get(url)
            return True
        except WebDriverException as e:
            if "tab crashed" in str(e) or "invalid session id" in str(e) or "no such window: target" in str(e) and attempt < max_retries - 1:
                print(f"Tab crashed, retrying ({attempt + 1}/{max_retries})...")
                driver.quit()
                driver = initialize_driver()
                time.sleep(2)  # Brief pause between retries
                continue
            raise
    return False

def search_fill_clean(arr) -> list:
    driver = initialize_driver()
    driver.maximize_window()

    time.sleep(2)
    
    try:
        # Accept cookies with retry logic
        for _ in range(3):
            try:
                if safe_get(driver, HOME_PAGE_URL):
                    accept_cookies(driver, 10, COOKIES_ACCEPT_DIV)
                    break
            except Exception:
                continue

        result = []
        
        for entry in arr:
            current_time = datetime.now().strftime("%H:%M")
            if entry["start_time"] <= current_time:
                continue

            search_name = name_in_url_format(entry["teams"].split(" vs ")[0])
            url = SEARCH_PAGE_STATIC_URL + search_name
            
            for attempt in range(3):
                try:
                    if not safe_get(driver, url):
                        continue
                        
                    driver.execute_script("window.scrollBy(0, 200)")
                    wait = WebDriverWait(driver, 50)
                    
                    match = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "event-markets-count-4"))
                    )
                    
                    try:
                        _event_id = WebDriverWait(match, 50).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "event-date-id"))
                        ).text.split(" ")[5]
                        _event_id = int(_event_id)
                    except Exception:
                        continue

                    if _event_id == entry['event_id']:
                        more_markets = WebDriverWait(match, 50).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "event-extra"))
                        )
                        more_markets.click()

                        try:
                            markets = wait.until(
                                EC.presence_of_element_located((By.CLASS_NAME, "event-market-columns-2"))
                            )
                            markets_result = markets.text.split("\n")

                            if markets_result[0] == "BOTH TEAMS TO SCORE":
                                odds = {
                                    "YES": float(markets_result[2]),
                                    "NO": float(markets_result[4])
                                }
                                entry["SP"] = {"GG": odds["YES"], "NO_GG": odds["NO"]}
                                result.append(entry)
                                break  # Success - exit retry loop
                                
                        except Exception:
                            continue
                            
                except Exception as e:
                    if "tab crashed" in str(e) or "invalid session id" in str(e) or "no such window: target" in str(e) and attempt < 2:
                        print(f"Tab crashed on entry {entry['event_id']}, retrying...")
                        driver.quit()
                        driver = initialize_driver()
                        time.sleep(2)
                        continue
                    break
                    
    finally:
        driver.quit()
        
    return result

def name_in_url_format(name) -> str:
    return name if " " not in name else name.replace(" ", "%20")

def accept_cookies(drv, _timeout, cookies_div) -> None:
    try:
        cookie_div = WebDriverWait(drv, _timeout).until(
            EC.presence_of_element_located((By.ID, cookies_div))
        )
        if cookie_div:
            cookie_button = drv.find_element(By.TAG_NAME, "button")
            cookie_button.click()
    except Exception:
        print("Cookie acceptance failed or not required")

if __name__ == "__main__":
    arr = []  # Your input array here
    x = search_fill_clean(arr)
    for idx, item in enumerate(x):
        print(f"{idx} : {item}")