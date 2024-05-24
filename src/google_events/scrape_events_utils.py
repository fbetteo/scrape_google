from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import re
from datetime import datetime, timedelta

import time


def get_google_events(city):

    options = Options()
    options.headless = True  # Run headless browser (no GUI)

    driver = webdriver.Chrome(options=options)

    # Define the search URL
    query = f"events in {city}&gl=us&hl=en&ibp=htl;events"
    url = f'https://www.google.com/search?q={query.replace(" ", "+")}'

    # Load the page
    driver.get(url)

    # To scroll down and load more events. Lazy loading of events
    def scroll_down_inner_element(driver, jsname, num_scrolls):
        scrollable_element = driver.find_element(
            By.CSS_SELECTOR, f"[jsname='{jsname}']"
        )
        for _ in range(num_scrolls):
            # Scroll the full height of the scrollable element
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element
            )
            # time.sleep(2)  # Wait for new elements to load. We can try removing this

    try:
        event_list = []
        # Max number of scrolls
        for scroll in range(3):
            if scroll != 0:
                # that jsnaame is the class of the div element that contains the events. First time we don't scroll, then we do one scrolling.
                scroll_down_inner_element(driver, "CaV2mb", 1)

                # Wait until there are 7 elements loaded with date - I think 7 is the amount I can see locally.
                WebDriverWait(driver, timeout=10).until(
                    lambda d: len(
                        [
                            elem
                            for elem in d.find_elements(By.CSS_SELECTOR, "div.wsnHcb")
                            if len(elem.text) > 0
                        ]
                    )
                    > 6
                )

            # Find events
            events = [
                event
                for event in driver.find_elements(By.CSS_SELECTOR, "div.odIJnf")
                if len(event.find_element(By.CSS_SELECTOR, "div.YOGjf").text) > 0
            ]

            # Loop and extract information
            for event in events:
                try:
                    title = event.find_element(By.CSS_SELECTOR, "div.YOGjf").text
                    event_data = event.find_element(By.CSS_SELECTOR, "div.SHrHx").text
                    event_day = event.find_element(By.CSS_SELECTOR, "div.UIaQzd").text
                    event_month = event.find_element(By.CSS_SELECTOR, "div.wsnHcb").text
                    img_elements = event.find_element(By.TAG_NAME, "img").get_attribute(
                        "src"
                    )

                    # Extract the src attributes
                    # src_list = [img.get_attribute("src") for img in img_elements]
                    event_list.append(
                        {
                            "title": title,
                            "event_day": event_day,
                            "event_month": event_month,
                            "event_data": event_data,
                            "img": img_elements,
                        }
                    )
                except Exception as e:
                    print(f"Error extracting event: {e}")
    except Exception as e:
        print(f"Error: {e}")

    driver.quit()
    return event_list


def get_google_search_results_count(queries):
    options = Options()
    options.headless = True  # Run headless browser (no GUI)

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    search_numbers = []
    for query in queries:
        # Define the search URL
        url = f'https://www.google.com/search?q={query.replace(" ", "+")}&gl=us&hl=en&tbs=qdr:w'  # tbs=qdr:w sets the time range to last week

        # Load the page
        driver.get(url)
        # time.sleep(2)  # Wait for the page to load (adjust as necessary)

        # Extract the number of search results
        try:
            results_stats = driver.find_element(By.ID, "result-stats").text
            print(f"Results Stats: {results_stats}")
            search_numbers.append(results_stats)
        except Exception as e:
            print(f"Error retrieving results stats: {e}")
            search_numbers.append("Error retrieving results stats")

    driver.quit()
    return search_numbers
