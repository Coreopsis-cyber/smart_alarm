"""
    Retrieves local weather data from API "api.openweathermap.org".
"""
import json
import logging
import requests
import global_variables

logging.basicConfig(filename='sys.log',encoding= 'utf-8', level=logging.DEBUG)

def get_weather() -> dict:
    """
        Gets weather data based on the perameters set in the config file, then formats
        the data for the annoucement and notifications.

        Uses an API containing up to date weather information for the area specified in
        the config file
        After the data is filtered it is formatted into a user friendly string.
        It is then added to global variables old_weather_notifs and current_notif
        if not already there.

        Global variables:
        old_weather_notifs = a list (of dictionaries) containing all the weather info collected
         previously.
        current_notifs = a lits (of dictionaries) containing current notifications (weather,
        COVID and news).

        Returns:
        A dictionary with current weather info.

    """
    base_url= 'http://api.openweathermap.org/data/2.5/weather?q='
    #Getting the region and the API key from the config.json file
    with open("config.json", "r") as config_file:
        json_config = json.load(config_file)
        weather_config = json_config['weather_api']
        api_key = weather_config["API_key_weather"]
        city = weather_config["city"]
        unit = weather_config["unit"]
    #Creating the full URL using user perameters
    complete_url = base_url + city + "&unit=" + unit + "&appid=" + api_key
    #Getting JSON file of weather info
    response = requests.get(complete_url)
    if response.status_code == 200:
        weather_json = response.json()
        try:
            main_weather = weather_json["weather"]
            forecast_description = main_weather[0]["description"]
            main = weather_json["main"]
            temp = main["temp"]
            feels_like = main["feels_like"]
        except KeyError as excep:
            logging.error("%s Valid JSON file cannot be retrieved as likely invalid API key", excep)
            forecast_description = "Unable to get weather info"
        weather_notification = {"title": "Weather Update", "content": " Today's forecast is " + forecast_description + ". The average temperature is " + str(int(temp -273)) + " degrees celsius. It feels like " + str(int(feels_like -273)) + " degrees celsius."}
    if weather_notification not in global_variables.old_weather_notifs:
        global_variables.old_weather_notifs.append(weather_notification)
        global_variables.current_notifs.insert(0,weather_notification)
    return weather_notification
