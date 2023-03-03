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
        ex_wait = WebDriverWait(driver, 5)

        # go to the search page
        search_link = ex_wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Search"))
        )
        search_link.click()

        # work with the input
        input_container = ex_wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "search__input__container"
                                            ))
        )
        _input = input_container.find_element(By.TAG_NAME, "input")
        _input.send_keys(arr[0]["teams"].split(
            " vs ")[0])
        _input.send_keys(Keys.RETURN)

        # get target results:
        # Affirm it is the target event.
        event_rows = ex_wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "prebet-match"))
        )
        for event in event_rows:
            time_div = event.find_element(By.CLASS_NAME, "time")
            start_time = time_div.text.strip().split(", ")[1]

            if start_time == arr[0]["start_time"]:
                break

        # get the right markets.
        more_markets_link = WebDriverWait(event, 5).until(
            EC.element_to_be_clickable((By.TAG_NAME, "a"))
        )
        more_markets_link.click()

        market_rows = ex_wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "market"))
        )

        odds = {}
        is_found = False
        for market in market_rows:
            # target markets found
            market_text = market.text.split("\n")
            if market_text[0] == "Both Teams To Score (Gg/ng)":
                odds["GG"] = float(market_text[2])
                odds["NO_GG"] = float(market_text[4])
                is_found = True
                break

        if is_found == False:
            # no gg markets found, thus remove the whole event from the input arr
            pass

        # Update entry:
        arr[0]["BK"] = {
            "GG": odds["GG"],
            "NO_GG": odds["NO_GG"]
        }

    finally:
        driver.quit()

    return arr


print(add_betika_data(sample_input_arr))
