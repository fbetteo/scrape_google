import pandas as pd
from src.google_flight_analysis.scrape import *
from src.google_flight_analysis.cache import *
import time
from datetime import date, timedelta

# to track the time of execution
start_time = time.time()

today = date.today()
start_date = date.today() + timedelta(days=1)  # change for today
num_days = 30
origin = "CAI"
destination = "JED"


date_list = [
    (start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)
]

list_of_dates = [Scrape(origin, destination, date_) for date_ in date_list]

ScrapeObjects(list_of_dates)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Function execution time: {elapsed_time} seconds")


combined_df = pd.concat([item.data for item in list_of_dates], ignore_index=True)

combined_df
combined_df.to_csv(
    f"{origin.lower()}_{destination.lower()}_scraping/{origin.lower()}_{destination.lower()}_{today}.csv",
    index=False,
)


####
