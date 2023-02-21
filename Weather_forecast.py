from datetime import datetime
from distutils.log import error
import requests
import os

# Logging is build in module in Python
import logging 

# This configuration sets the logging level to DEBUG. Messages will be logged.

logging.basicConfig(filename='app.log', level=logging.DEBUG)

# The value of an environment variable. Storing information.
# My EnvVariable from (My PC)
# key is retrieved from an environment variable called 'FORECAST_API_KEY using os.environ.get function.

key = os.environ.get('FORECAST_API_KEY') 
print(key)

# Link from OpenWeatherMap.org \for 5 days with data every 3 hours by city name.
"""
1: request to the OpenWeatherMap API.
2: The query has the parameters that will be sent along with the request.
3: The parameter include name of city , units of measurement and the API KEY.
4: The requests.get function is used to send an HTTP GET request to the API.
5: jSON data is stored in the 'data' variable.

"""

url = 'https://api.openweathermap.org/data/2.5/forecast'   
query = {'q': 'minneapolis,us' , 'units': 'imperial', 'appid':key}
data = requests.get(url, params=query).json()


# Main entry point of the program 
# get location; prompt the user for the name of a city and the two-letter country code.
# get_current_weather; Is called with the location and the API key parameters from OpenWeatherMap.
# also, contain the weather data and any errors during the API request.

# logging.error; prints a message indicating that the weather data could not be retrieved.
# get temp; display the weather forecast information for the specified location (when the user set the location in the program.)

def main():
    location = get_location()
    weather_data, error = get_current_weather(location, key)
    if error:
        logging.error(error)
        print('Sorry, could not get weather')
    else:
        get_temp(weather_data)


# Here the program uses 'def get location' to ask the user questions and is based on the city and
# the 2 letters of the country code (location is returned)

def get_location():
    city, country = '',''
    while len(city) == 0:
        city = input('Enter the name of the city: ').strip()

    while len(country) != 2 or not country.isalpha():
        country = input('Enter the 2-Letter country code: ').strip()

    location = f'{city}, {country}'
    return location



def get_current_weather(location , key):
    try:
        query = {'q': location, 'units':'imperial','appid':key}
        response = requests.get(url, params=query)
        response.raise_for_status()
        data = response.json()
        return data, None
    except Exception as ex:
        print(ex)
        logging.debug(response.text)
        print(response.text)
        return None, ex

def get_temp(weather_data):
    try:
        list_of_forecast = weather_data['list']
        print('%-20s %-14s %-18s %-10s ' % ('Date', 'Temperature F', 'Description', 'Wind speed'))
        print('-'*65)
        for forecast in list_of_forecast:
            temp = forecast['main']['temp']
            timestamp = forecast['dt']
            desc = forecast['weather'][0]['description']
            wind = forecast['wind']['speed']

            forecast_date = datetime.fromtimestamp(timestamp)
            print('%-20s %-14s %-18s %-10s' % (forecast_date, temp, desc, wind))
    
    except KeyError:
        print('Sorry, no weather data')
        return 'Unknown'
    
if __name__ == '__main__':
    # The program run, it should only print - user-friendly messages.
    logging.info(f'thanks,we get the weather') 
    main()

    
