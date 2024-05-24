import pandas as pd
import src.google_events.scrape_events_utils as utils

# https://www.google.com/search?q=events+in+Buenos+Aires&gl=us&hl=en&ibp=htl;events

# Currently running here. Just change the city. 
# We can make this a script to run with city as a parameter
# We can modify the quuery to include only the next month or things like that , although big events in the future seem useful.

city = "Buenos Aires"

events = utils.get_google_events(city)

# Print the event information
for event in events:
    print(f"Event: {event['title']}")
    print(f"Date & Time: {event['event_data']}")
    print("-" * 40)


# Create the query including the city name only for the events with a title
events_names = [
    event["title"] + " " + city for event in events if len(event["title"]) > 0
]
# #
search_importance = utils.get_google_search_results_count(events_names)


### CREATE FINAL TABLE
full_events = [event for event in events if len(event["title"]) > 0]
event_title = [event["title"] for event in full_events]
event_day = [event["event_day"] for event in full_events]
event_month = [event["event_month"] for event in full_events]
event_img = [event["img"] for event in full_events]

final_df = pd.DataFrame(
    {
        "Event": event_title,
        "city": city,
        "day": event_day,
        "month": event_month,
        "img": event_img,
        "search_importance": search_importance,
        "query_date": pd.Timestamp("today").strftime("%Y-%m-%d"),
    }
)

final_df

final_df.to_csv(f"events_{city.lower().replace(" ", "")}.csv", index=False)
