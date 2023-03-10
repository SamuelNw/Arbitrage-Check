# Function to clean and add more details to the result received above.
"""
This function (search_fill_clean) loops through the general data result and does the following on each entry:
    - Searches for the specific event on sportpesa.com. 
    - If it finds the event and it is yet to start, get the desired markets (GG and NO_GG) and update that
    entry to include this information as an object.
    - Since some events lack this market, it scraps that whole entry from the resultant array as it is of no use.
    - Returns a comprehensive array of dictionaries with teams, start_time, ID, sp_markets (another dictionary).

    # Input --> [{'teams': 'AL-SHABBAB vs AL-BUDAIYA', 'start_time': '18:30', 'event_id': 3226}]
    # Output --> [{'teams': 'AL-SHABBAB vs AL-BUDAIYA', 'start_time': '18:30', 'event_id': 3226, 'SP': {'GG': 1.97, 'NO_GG': 1.69}}...]
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Home Page
HOME_PAGE_URL = "https://www.ke.sportpesa.com/sports/football?sportId=1&section=highlights"
# Search Page Static url
SEARCH_PAGE_STATIC_URL = "https://www.ke.sportpesa.com/search?sportId=1&text="
# Class name to the cookies div.
COOKIES_ACCEPT_DIV = "cookies-law-info-content"


# Create a new ChromeDriver service object
service = webdriver.chrome.service.Service(
    executable_path=ChromeDriverManager().install())

# Start a new Chrome browser instance using the service object
driver = webdriver.Chrome(service=service)


def search_fill_clean(arr) -> list:

    driver.get(HOME_PAGE_URL)
    driver.maximize_window()

    accept_cookies(driver, 5, COOKIES_ACCEPT_DIV)

    try:
        for entry in arr:
            # Only search using the first team
            search_name = name_in_url_format(entry["teams"].split(" vs ")[0])

            driver.get(SEARCH_PAGE_STATIC_URL + search_name)
            driver.execute_script("window.scrollBy(0, 100)")
            driver.implicitly_wait(5)

            wait = WebDriverWait(driver, 10)
            match = wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "event-markets-count-4"))
            )

            # Also, if the game has started, the event-markets-count-4 is no longer present.
            if not match:
                print(f"Match {entry['teams']} has started. Removing it..")
                arr.remove(entry)
                continue

            # Affirm that it is the same event as the one intended (By checking the ID).
            _event_id = WebDriverWait(match, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "event-info"))).text.split("\n")[2]
            _event_id = int(_event_id.split(" ")[1])
            if _event_id == entry['event_id']:
                more_markets = WebDriverWait(match, 15).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "event-extra")))
                more_markets.click()

                # Search for divs with the gg market
                """
                As far as I know, the gg/nogg markets div is not the only one with the below class name
                but it shall always be the first div on the page, as long as that event has these markets. Thus, to check
                and eliminate events without this market, the first value of the returned elements text has to be:
                'BOTH TEAMS TO SCORE'.
                """
                markets = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "event-market-columns-2"))
                )

                markets_result = markets.text.split("\n")

                if markets_result[0] != "BOTH TEAMS TO SCORE":
                    arr.remove(entry)
                    print(
                        f"\n{entry['teams']} - has no desired market, thus removed.")
                else:
                    odds = {"YES": 0, "NO": 0}
                    odds["YES"] = float(markets_result[2])
                    odds["NO"] = float(markets_result[4])

                    # Update the entry with the newly fetched values
                    entry["SP"] = {
                        "GG": odds["YES"],
                        "NO_GG": odds["NO"]
                    }

            else:
                # This particular event has probably already started and is not in the prematch bet events.
                arr.remove(entry)
                print(
                    f"Removed the event {entry['teams']} from the array. It might have already started.")
                continue

    finally:
        driver.quit()
        return arr

    # return arr


# Get an input format of the search term as required.
def name_in_url_format(name) -> str:
    """
    Info: The dynamic part of the search url.
    - If the name has no spaces in it, it goes as is.
    - If any space is present, replace it with the string '%20' --> what the target site does.
    """
    if not " " in name:
        return name
    return name.replace(" ", "%20")


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


if __name__ == "__main__":
    arr = []
    search_fill_clean(arr)
