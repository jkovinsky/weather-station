
import time
import json
import requests


#
# Update this to your weather feed
WEATHER_FEED_ENDPOINT = "https://api.weather.gov/points"



def get_local_station(latitude, longitude):
    try:
        response  = requests.get(f"{WEATHER_FEED_ENDPOINT}/{latitude},{longitude}")
        data = response.json()
        local_forecast_url = data['properties']['forecast']
        print(f"Local forecast url successfully fetched: {local_forecast_url}")

        return local_forecast_url
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

        return "unexpected_error"


def get_last_data(station_url):
    try:
        response = requests.get(station_url)
        data = response.json()

        with open("output.json", "w") as f:
            json.dump(data, f, indent=2)

        return data
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

        return "unexpected_error"
        

def get_forecast(lat, lon):
    url = get_local_station(lat, lon)
    data = get_last_data(url)
    return data


def get_periods(forecast):
    periods = forecast['properties']['periods']
    return periods



# get_forecast(37.7995, -122.4089)

