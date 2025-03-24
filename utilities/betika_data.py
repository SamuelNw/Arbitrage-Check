# This script searches and adds Betika data to the specific prematch events.
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from utilities.helpers import clean_search_input, verify


# Betika Home Page Url
HOME_PAGE_URL = "https://www.betika.com/en-ke/"


driver_path = "/Users/sam/Desktop/Cipher/Ciphy/Arbitrage-Check/drivers/chromedriver"

# Create a service object
service = Service(executable_path=driver_path)

# Create a driver with the service:
driver = webdriver.Chrome(service=service)


def add_betika_data(arr) -> list:
    driver.get(HOME_PAGE_URL)
    driver.maximize_window()

    # Create a new array with only valid entries:
    result = []

    try:
        for entry in arr:
            # Skip and Eliminate any started events.
            current_time = datetime.now().strftime("%H:%M")
            if entry["start_time"] < current_time:
                continue

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
            _input = WebDriverWait(input_container, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "input")))
            _input.clear()
            search_term = clean_search_input(entry["teams"])
            _input.send_keys(search_term)
            _input.send_keys(Keys.RETURN)

            # get target results:
            # Affirm it is the target event.
            market_rows = None
            try:
                event_rows = ex_wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "prebet-match"))
                )

                if event_rows:
                    for event in event_rows:
                        time_div = event.find_element(
                            By.CLASS_NAME, "time")
                        start_time = time_div.text.split(
                            "\n")[1].split(", ")[1]

                        if start_time == entry["start_time"]:
                            # team names are the 3rd and 4th elements:
                            entry_text = list(event.text.split("\n"))
                            team_names = entry_text[2:4]

                            # ONLY CARRY ON IF THE EVENTS VERIFY
                            if verify(entry, search_term, team_names):
                                # get the right markets.
                                more_markets_link = WebDriverWait(event, 5).until(
                                    EC.element_to_be_clickable(
                                        (By.TAG_NAME, "a"))
                                )
                                more_markets_link.click()

                                market_rows = ex_wait.until(
                                    EC.presence_of_all_elements_located(
                                        (By.CLASS_NAME, "market"))
                                )
                                break
                        else:
                            continue
                    if market_rows == None:
                        driver.back()
                        continue
            except Exception:
                pass

            odds = {}
            is_found = False

            if market_rows:
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
                if odds:
                    entry["BK"] = {
                        "GG": odds["GG"],
                        "NO_GG": odds["NO_GG"]
                    }

                    result.append(entry)
            continue

    finally:
        driver.quit()
    
    return result


if __name__ == "__main__":
    arr = []
    x = add_betika_data(arr)
    for idx, item in enumerate(x):
        print(f"{idx} : {item}")
