# This script searches and adds Betika data to the specific prematch events.
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import random

# Betika Home Page Url
HOME_PAGE_URL = "https://www.betika.com/en-ke/"


service = webdriver.chrome.service.Service(
    executable_path=ChromeDriverManager().install()
)

driver = webdriver.Chrome(service=service)


def add_betika_data(arr) -> list:
    driver.get(HOME_PAGE_URL)
    driver.maximize_window()

    try:
        for entry in arr:
            # Skip and Eliminate any started events.
            current_time = datetime.now().strftime("%H:%M")
            if entry["start_time"] < current_time:
                print(
                    f"{entry['teams']} has already started. 'BK' value shall equal None.")
                entry["BK"] = None
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
            _input.send_keys(clean_search_input(entry["teams"]))
            _input.send_keys(Keys.RETURN)

            # get target results:
            # Affirm it is the target event.
            try:
                event_rows = ex_wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "prebet-match"))
                )
                if event_rows:
                    for event in event_rows:
                        time_div = event.find_element(By.CLASS_NAME, "time")
                        start_time = time_div.text.split(
                            "\n")[1].split(", ")[1]

                        if start_time == entry["start_time"]:
                            # get the right markets.
                            more_markets_link = WebDriverWait(event, 5).until(
                                EC.element_to_be_clickable((By.TAG_NAME, "a"))
                            )
                            more_markets_link.click()

                            market_rows = ex_wait.until(
                                EC.presence_of_all_elements_located(
                                    (By.CLASS_NAME, "market"))
                            )
                            break
                        else:
                            print(
                                f"{entry['teams']} is absent. Setting value to None")
                            entry["BK"] = None
            except:
                print(
                    f"No results for that {entry['teams']} on betika. 'BK' value shall equal None")
                entry["BK"] = None
                continue

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
                print(
                    f"Gg markets for {entry['teams']} not found. 'BK' shall equal None.")
                entry["BK"] = None
                continue

            # Update entry:
            if odds:
                entry["BK"] = {
                    "GG": odds["GG"],
                    "NO_GG": odds["NO_GG"]
                }
            driver.get(HOME_PAGE_URL)

    finally:
        driver.quit()
        return arr


# Clean search name
def clean_search_input(string) -> str:
    """
    Info: The Betika site has the following limitations regarding team names searched:
        - It only returns results for the accurately spelt names.
        - No word under 4 characters really returns accurate results.
        - Mostly shortens team names with more than one word (If both names are longer
        than 4 characters each, they shorten the longest and use the other).
        - Strings like 'U20', 'U23' are unacceptable

    Implemented solution:
        - First check the name of the first team:
            - if it has no spaces and is longer than four characters, use it.
            - if it has a space, get the longest word of those present, and these
            longest words must be longer than 3 characters and shorter than 10 
            characters, else just use the next word.
        - If none of those work, do the same check for the second name.
        - Randomly pick any three letter word available at that instance and take chances on it, lol.
    """

    str_arr = string.split(" vs ")
    first_name = str_arr[0]
    second_name = str_arr[1]

    some_exceptions = ["SOUTH", "NORTH", "WEST", "EAST"]

    # check first name:
    if not " " in first_name and len(first_name) > 3:
        return first_name

    if " " in first_name:
        # for cases such as "SOUTH KOREA U23"
        for name in some_exceptions:
            if name in first_name.split(" "):
                return f"{first_name.split(' ')[0]} {first_name.split(' ')[1]}"

        longest_word = max(first_name.split(" "), key=len)
        len_longest = len(longest_word)
        if len_longest >= 4 and len_longest <= 9:
            return longest_word

    # Check second name
    if not " " in second_name and len(second_name) > 3:
        return second_name

    if " " in second_name:
        longest_word = max(second_name.split(" "), key=len)
        if len(longest_word) >= 4:
            return longest_word

    # Worst case scenario eg --> "FC OSS vs FC AIK"
    random_idx = random.randint(0, 1)
    return max(str_arr[random_idx].split(" "), key=len)
