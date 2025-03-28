# Get the data for a minimum of 50 PreMatch events from sportpesa.com
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from . import search_fill_clean_sp as sfp

# Daily PreMatch events link.
DAILY_EVENTS_URL = "https://www.ke.sportpesa.com/en/sports-betting/football-1/today-games/"
# Next Page Static url
NEXT_PAGE_STATIC_URL = "https://www.ke.sportpesa.com/en/sports-betting/football-1/today-games/?paginationOffset="
# Class name to the cookies div.
COOKIES_ACCEPT_DIV = "cookies-law-info-content"

driver_path = "/Users/sam/Desktop/Cipher/Ciphy/Arbitrage-Check/drivers/chromedriver"

# Create a service object
service = Service(executable_path=driver_path)

# Create a driver with the service:
driver = webdriver.Chrome(service=service)


"""
This function (get_general_data) returns an array of events with only general data.
General data here refers to:
    - Involved teams in an event. 
    - Starting time of the event. 
    - ID of the said event.
"""


def get_sportpesa_data() -> list:

    driver.get(DAILY_EVENTS_URL)
    driver.maximize_window()

    # Accept Cookies --> cause why not do this too.
    accept_cookies(driver, 5, COOKIES_ACCEPT_DIV)

    try:
        # Scroll to the bottom to ensure all events load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Get a list with the number of available pages of events.
        pagination = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "event-list-pagination"))
        )

        next_buttons = pagination.find_elements(By.CLASS_NAME, "ng-binding")

        available_pages = [item.text for item in next_buttons]
        a_len = len(available_pages)
        print(
            f"Found {a_len} pages. Expected entries to work on should be at least --> {(a_len - 1) * 15}")

        # Initiate an empty array to append dictionaries containing event info
        result = []

        event_totals = 15

        try:
            # Get content from as many pages as ones available
            for idx in range(a_len):

                # Scroll to the bottom to ensure all events load
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight)")

                # Get all the event rows
                event_rows = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "event-markets-count-4")))

                # Get the start_time, ID and names of teams in each the match
                for event in event_rows:
                    event_info = event.find_element(
                        By.CLASS_NAME, "event-date-id")
                    entry_data = event_info.text.split(" ")

                    event_names = event.find_element(
                        By.CLASS_NAME, "event-names")
                    entry_names = event_names.text.split("\n")

                    entry = {}
                    entry["teams"] = f"{entry_names[0]} vs {entry_names[1]}"
                    entry["start_time"] = f"{entry_data[2]}"
                    entry["event_id"] = int(entry_data[5])

                    result.append(entry)

                # Get the URL for the next page
                next_page_url = NEXT_PAGE_STATIC_URL + str(event_totals)

                # Navigate to the next page
                driver.get(next_page_url)

                event_totals += 15          # Total number of events sportpesa loads per page

                if idx == a_len - 1:
                    driver.quit()
                else:
                    continue
        finally:
            # refill result if result is not empty
            if result:
                print(
                    f"Working with a list of {len(result)} entries. Hang tight...")
                result = sfp.search_fill_clean(result)
                print(
                    f"Collected {len(result)} valid entries from sportpesa, moving on to betika...")
            else:
                print("result is empty or invalid.")

    finally:
        driver.quit()

    return result


# Accepting cookies on this site:
def accept_cookies(drv, _timeout, cookies_div) -> None:
    cookie_div = WebDriverWait(drv, _timeout).until(
        EC.presence_of_element_located((By.ID, cookies_div))
    )

    if cookie_div:
        cookie_button = driver.find_element(By.TAG_NAME, "button")
        cookie_button.click()
    else:
        print("Never found any cookie laws.")


if __name__ == "__main__":
    res = get_sportpesa_data()

    for idx, entry in enumerate(res):
        print(f"{idx} : {entry}")
