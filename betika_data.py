# This script searches and adds Betika data to the specific prematch events.
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Betika Home Page Url
HOME_PAGE_URL = "https://www.betika.com/en-ke/"


service = webdriver.chrome.service.Service(
    executable_path=ChromeDriverManager().install()
)

driver = webdriver.Chrome(service=service)

sample_input_arr = [
    {
        "teams": "REAL SOCIEDAD vs CADIZ CF",
        "start_time": "23:00",
        "event_id": 5871,
        "SP": {"GG": 2.38, "NO_GG": 1.51}
    },
    {
        "teams": "JAPAN U20 vs CHINA U20",
        "start_time": "13:00",
        "event_id": 2083,
        "SP": {"GG": 2.50, "NO_GG": 1.42}
    }
]


def add_betika_data(arr):
    driver.get(HOME_PAGE_URL)
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 5)

        # go to the search page
        search_link = wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Search"))
        )
        search_link.click()
        time.sleep(2)

        # work with the input

    finally:
        driver.quit()

    return arr


add_betika_data(sample_input_arr)
