# Get the data for a minimum of 50 PreMatch events from sportpesa.com
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import search_fill_clean_sp

# Daily PreMatch events link.
DAILY_EVENTS_URL = "https://www.ke.sportpesa.com/en/sports-betting/football-1/today-games/"
# Next Page Static url
NEXT_PAGE_STATIC_URL = "https://www.ke.sportpesa.com/en/sports-betting/football-1/today-games/?paginationOffset="
# Class name to the cookies div.
COOKIES_ACCEPT_DIV = "cookies-law-info-content"

# Create a new ChromeDriver service object
service = webdriver.chrome.service.Service(
    executable_path=ChromeDriverManager().install())

# Start a new Chrome browser instance using the service object
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

        # Initiate an empty array to append dictionaries containing event info
        result = []

        event_totals = 15
        # Get content from as many pages as ones available
        for idx in range(len(available_pages[1:])):

            # Get all the event rows
            event_rows = driver.find_elements(
                By.CLASS_NAME, "event-markets-count-4")

            # Get the start_time, ID and names of teams in each the match
            for event in event_rows:
                event_info = event.find_element(By.CLASS_NAME, "event-info")
                entry_data = event_info.text.split("\n")

                event_names = event.find_element(By.CLASS_NAME, "event-names")
                entry_names = event_names.text.split("\n")

                entry = {}
                entry["teams"] = f"{entry_names[0]} vs {entry_names[1]}"
                entry["start_time"] = f"{entry_data[0]}"
                entry["event_id"] = int(entry_data[2].split(" ")[1])

                result.append(entry)

            # Get the URL for the next page
            next_page_url = NEXT_PAGE_STATIC_URL + str(event_totals)

            # Navigate to the next page
            driver.get(next_page_url)

            event_totals += 15          # Total number of events sportpesa loads per page

            if idx == len(available_pages) - 1:
                driver.quit()

        # refill result if result is not empty
        if result:
            print(
                f"Working with a list of {len(result)} entries. Hang tight...")
            result = search_fill_clean_sp.search_fill_clean(result)
            print("Process Completed.")
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
    return


res = get_sportpesa_data()

for idx, entry in enumerate(res):
    print(f"{idx} : {entry}")
