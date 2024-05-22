import pytest
import pandas as pd
from pathlib import Path
import os


from src.google_flight_analysis.scrape import *
from src.google_flight_analysis.cache import *

res1 = Scrape("LGA", "RDU", "2024-05-25", "2024-06-15")

ScrapeObjects(res1)

import time

start_time = time.time()
cai_jed = Scrape("CAI", "JED", "2024-05-26")
ScrapeObjects(cai_jed)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Function execution time: {elapsed_time} seconds")


### List for scraping
from datetime import date, timedelta

start_time = time.time()
start_date = date(2024, 5, 25)
num_days = 30
date_list = [
    (start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)
]
list_of_dates = [Scrape("CAI", "JED", date) for date in date_list]
ScrapeObjects(list_of_dates)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Function execution time: {elapsed_time} seconds")


combined_df = pd.concat([item.data for item in list_of_dates], ignore_index=True)

combined_df
