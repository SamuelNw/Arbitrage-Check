# This script searches and adds Betika data to the specific prematch events.
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time
import re


# Betika Home Page Url
HOME_PAGE_URL = "https://www.betika.com/en-ke/"


driver_path = "/Users/sam/Desktop/Cipher/Ciphy/Arbitrage-Check/drivers/chromedriver"

# Create a service object with anti-detection flags and memory optimizations
service = Service(executable_path=driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')

# Create a driver with the service:
driver = webdriver.Chrome(service=service)


def add_betika_data(arr) -> list:
    driver.get(HOME_PAGE_URL)
    driver.maximize_window()
    time.sleep(2)  # Wait for the page to load

    # Create a new array with only valid entries:
    result = []

    try:
        for entry in arr:
            # Skip and Eliminate any started events.
            current_time = datetime.now().strftime("%H:%M")
            if entry["start_time"] < current_time:
                continue

            ex_wait = WebDriverWait(driver, 10)

            # go to the search page
            search_link = ex_wait.until(
                EC.visibility_of_element_located((By.LINK_TEXT, "Search"))
            )
            search_link.click()
            time.sleep(1)

            # work with the input
            input_container = ex_wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "search__input__container"))
            )
            _input = WebDriverWait(input_container, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "input")))

            """
            - Instead of finding an optimal name to use for the search, I'll
            search using each of the individual strings
            in the teams string (As long as they are more than 3
            characters). So if {'teams': 'ALIANZA ATLETICO vs CUSCO FC'},
            I'll use the following:
            ["ALIANZA", "ATLETICO", "CUSCO"]
            - If any of these words return the expected results, we use those
            and move on.
            """

            # Extract search terms (words > 3 characters from both team names)
            team1, team2 = entry["teams"].split(" vs ")
            search_terms = []

            # Add words from first team
            for word in team1.split():
                if len(word) > 3:
                    search_terms.append(word)

            # Add words from second team (only if first team search fails)
            for word in team2.split():
                if len(word) > 3 and word not in search_terms:
                    search_terms.append(word)

            market_rows = None
            odds = {}
            is_found = False

            for search_term in search_terms:
                try:
                    _input.clear()
                    _input.send_keys(search_term)
                    _input.send_keys(Keys.RETURN)

                    event_rows = ex_wait.until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, "prebet-match"))
                    )

                    if not event_rows:
                        print(f"No events found for search term: {search_term}")
                        continue

                    # Check each event for matching time
                    for event in event_rows:
                        try:
                            time_div = event.find_element(
                                By.CLASS_NAME, "time")
                            start_time = time_div.text.split("\n")[1].split(
                                ", ")[1]

                            if start_time == entry["start_time"]:
                                # Verify the event using search terms and regex
                                event_teams = event.find_element(By.CLASS_NAME, "prebet-match__teams").text
                                matching_terms = [term for term in search_terms if re.search(rf"\b{term}\b", event_teams, re.IGNORECASE)]
                                if len(matching_terms) >= 2:  # Ensure at least two terms match
                                    # Open market details
                                    more_markets_link = WebDriverWait(
                                        event, 5).until(
                                        EC.element_to_be_clickable(
                                            (By.TAG_NAME, "a"))
                                    )
                                    more_markets_link.click()
                                    time.sleep(1)  # Allow markets to load

                                    # Find GG/NG markets
                                    market_rows = ex_wait.until(
                                        EC.presence_of_all_elements_located(
                                            (By.CLASS_NAME, "market"))
                                    )

                                    for market in market_rows:
                                        market_text = market.text.split("\n")
                                        if market_text[0] == \
                                                "Both Teams To Score (Gg/ng)":
                                            odds["GG"] = float(market_text[2])
                                            odds["NO_GG"] = float(market_text[4])
                                            is_found = True
                                            break

                                    if is_found:
                                        break  # Exit event loop if found

                                    driver.back()  # Go back if no GG market found

                        except Exception:
                            continue

                    if is_found:
                        break  # Exit search term loop if found

                    driver.back()  # Return to search page for next term
                    time.sleep(1)

                except Exception:
                    continue

            if is_found:
                entry["BK"] = {
                    "GG": odds["GG"],
                    "NO_GG": odds["NO_GG"]
                }
                result.append(entry)
            else:
                print(f"No matching markets found for: {entry['teams']}")

    finally:
        driver.quit()

    return result


if __name__ == "__main__":
    arr = []
    x = add_betika_data(arr)
    for idx, item in enumerate(x):
        print(f"{idx} : {item}")
