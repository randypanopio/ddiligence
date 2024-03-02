# script for testing new apis

import requests
import datetime
import json

# Define the base URL of the InSight API
base_url = 'https://api.nasa.gov/insight_weather/'

# Your NASA API key (Get your API key from NASA's website)
api_key = 'DEMO_KEY'

# Calculate dates
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=25*365)  # 25 years ago

def data():
    # Loop through each day and make API requests
    weather_data = []
    current_date = start_date
    while current_date <= end_date:
        # Format the date as needed by the API
        formatted_date = current_date.strftime('%Y-%m-%d')

        # Make API request for the specific date
        url = f"{base_url}?api_key={api_key}&feedtype=json&ver=1.0&feedtype=json&params=PRESSURE,TIMESTAMP"
        response = requests.get(url)

        if response.status_code == 200:
            # Append received data to the list
            weather_data.append({
                'date': formatted_date,
                'data': response.json()  # Store the response JSON data
            })
        else:
            print(f"Failed to fetch data for {formatted_date}")

        # Move to the next day
        current_date += datetime.timedelta(days=1)
    return weather_data


if __name__ == '__main__':
    print("mars weather data")
    url = url = f"{base_url}?api_key={api_key}&feedtype=json&ver=1.0&feedtype=json&params=PRESSURE,TIMESTAMP"
    print("url:\n" + url)
    response = requests.get(url)
    print(response)