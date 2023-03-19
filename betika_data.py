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

                count = 0
                if event_rows:
                    events = len(event_rows)
                    count += 1
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
                            if not count == events:
                                continue    # check all present events
                            else:
                                # go back one step
                                driver.back()
            except:
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
        - However, the name with the least number of spaces is one that is more likely to get
        the expected results.
        - Randomly pick any three letter word available at that instance and take chances on it, lol.
    """

    str_arr = string.split(" vs ")
    first_name = str_arr[0]
    second_name = str_arr[1]

    some_exceptions = ["SOUTH", "NORTH", "WEST", "EAST", "YOUTH"]

    # check first name:
    if not " " in first_name and len(first_name) > 3:
        return first_name

    # working with the name with least number of spaces:
    first_name_spaces = first_name.count(" ")
    second_name_spaces = second_name.count(" ")

    if " " in first_name and first_name_spaces < second_name_spaces:
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

    if " " in second_name and second_name_spaces < first_name_spaces:
        longest_word = max(second_name.split(" "), key=len)
        if len(longest_word) >= 4:
            return longest_word

    # Worst case scenario eg --> "FC OSS vs FC AIK"
    random_idx = random.randint(0, 1)
    return max(str_arr[random_idx].split(" "), key=len)


# Further event verification helper:
def verify(entry, term_searched, teams) -> bool:
    """
    INFO: This function checks if besides the search term selected,
    the other team's name is also in the current event being checked.
    """
    team_1 = teams[0].upper()
    team_2 = teams[1].upper()
    # case where both team names are just one word entries
    if not " " in team_1 and " " not in team_2:
        if term_searched == team_1:
            if team_2 in entry["teams"]:
                return True
        elif term_searched == team_2:
            if team_1 in entry["teams"]:
                return True

    # case where only one of the team names is a one word entry
    if " " in team_1 and not " " in team_2:
        if term_searched in team_1:
            if team_2 in entry["teams"]:
                return True
        elif term_searched == team_2:
            for name in list(team_1.split(" ")):
                if name in entry["teams"]:
                    return True
    elif " " in team_2 and not " " in team_1:
        if term_searched in team_2:
            if team_1 in entry["teams"]:
                return True
        elif term_searched == team_1:
            for name in list(team_2.split(" ")):
                if name in entry["teams"]:
                    return True

    # case where both team names are more than a word entry.
    if " " in team_1 and " " in team_2:
        if term_searched in team_1:
            for name in list(team_2.split(" ")):
                if name in entry["teams"]:
                    return True
        elif term_searched in team_2:
            for name in list(team_1.split(" ")):
                if name in entry["teams"]:
                    return True

    # if all the above cases dont match:
    return False


if __name__ == "__main__":
    arr = []
    x = add_betika_data(arr)
    for idx, item in enumerate(x):
        print(f"{idx} : {item}")
