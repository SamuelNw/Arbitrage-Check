# Get the data for a minimum of 50 PreMatch events from sportpesa.com
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Home Page
HOME_PAGE_URL = "https://www.ke.sportpesa.com/sports/football?sportId=1&section=highlights"
# Daily PreMatch events link.
DAILY_EVENTS_URL = "https://www.ke.sportpesa.com/sports/football?sportId=1&section=today"
# Next Page Static url
NEXT_PAGE_STATIC_URL = "https://www.ke.sportpesa.com/sports/football?sportId=1&section=today&paginationOffset="

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


def get_general_data():

    driver.get(DAILY_EVENTS_URL)
    driver.maximize_window()

    # Accept Cookies --> cause why not.
    cookie_div = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "cookies-law-info-content"))
    )

    if cookie_div:
        cookie_button = driver.find_element(By.TAG_NAME, "button")
        cookie_button.click()
    else:
        print("Never found any cookie laws.")

    try:
        # Scroll to the bottom to ensure all events load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Get a list with the number of available pages of events.
        pagination = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "event-list-pagination"))
        )

        pagination = driver.find_element(
            By.CLASS_NAME, "event-list-pagination")

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
                entry["event_id"] = entry_data[2]

                result.append(entry)

            # Get the URL for the next page
            next_page_url = NEXT_PAGE_STATIC_URL + str(event_totals)

            # Navigate to the next page
            driver.get(next_page_url)

            event_totals += 15          # Total number of events sportpesa loads per page

    finally:
        driver.quit()

    return result


# Second function to clean and add more details to the result received above.
def search_fill_clean(arr):
    pass