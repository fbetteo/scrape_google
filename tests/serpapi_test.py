## SERPAPI
import serpapi
import pandas as pd
from src.google_flight_analysis.scrape import *
from src.google_flight_analysis.cache import *
import time
from datetime import date, timedelta


# from serpapi import GoogleSearch
def serapi_individual_result_to_df(flight):
    flight_data = flight.get("flights", [{}])[0]
    departure_airport = flight_data.get("departure_airport", {})
    arrival_airport = flight_data.get("arrival_airport", {})
    df_data = {
        "departure_airport_name": departure_airport.get("name"),
        "departure_airport_id": departure_airport.get("id"),
        "departure_time": departure_airport.get("time"),
        "arrival_airport_name": arrival_airport.get("name"),
        "arrival_airport_id": arrival_airport.get("id"),
        "arrival_time": arrival_airport.get("time"),
        "duration": flight_data.get("duration"),
        "airplane": flight_data.get("airplane"),
        "airline": flight_data.get("airline"),
        "airline_logo": flight_data.get("airline_logo"),
        "travel_class": flight_data.get("travel_class"),
        "flight_number": flight_data.get("flight_number"),
        "legroom": flight_data.get("legroom"),
        "total_duration": flight.get("total_duration"),
        "price": flight.get("price"),
        "type": flight.get("type"),
    }
    return pd.DataFrame([df_data])


serpapi_key = "629374f42690d421071fda26468783fe6823bd1608a2746ada0824899090481c"


general_params = {
    "engine": "google_flights",
    "type": "2",
    "departure_id": "CAI",
    "arrival_id": "JED",
    "hl": "en",
    "gl": "us",
    "currency": "USD",
    "outbound_date": "2024-05-25",
    "api_key": serpapi_key,
}

start_time = time.time()
start_date = date(2024, 5, 25)
num_days = 30
date_list = [
    (start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)
]
daily_result = []
for future_date in date_list:
    general_params["outbound_date"] = future_date

    search = serpapi.GoogleSearch(general_params)
    results = search.get_dict()

    # asd = serapi_individual_result_to_df(results['best_flights'][0])

    best_flights = [
        serapi_individual_result_to_df(flight) for flight in results["best_flights"]
    ]

    other_flights = [
        serapi_individual_result_to_df(flight) for flight in results["other_flights"]
    ]

    daily_result.append(pd.concat(best_flights + other_flights, ignore_index=True))

total_result = pd.concat(daily_result, ignore_index=True)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Function execution time: {elapsed_time} seconds")

total_result.to_csv("serpapi_result.csv", index=False)
