"""
    Retrieves covid info from API using python library uk_covid19
    supplied by public health england
"""
import json
import logging
import global_variables
from uk_covid19 import Cov19API

logging.basicConfig(filename='sys.log',encoding= 'utf-8', level=logging.DEBUG)

def get_covid_info() -> dict :
    """
        Gets covid data based on users perameters in config file, then formats it
        for the use in notifications and announcements.

        areaCode = gives the area in the UK the user wants data for.
        cases_and_deaths = the specific type of covid data being retrieved.

        Local variables:
        filter_param = a list containing the areaCode from the config file.
        Global variables:
        covid_notif = a list (of dictionaries) on covid data previously collected.
        current_notif = a (list of dictionaries)  containing current notifications (weather,
        COVID and news).

        Returns:
        A string containing the formatted covid notification.

    """

    filter_param = []
    #Getting the parameters for the covid info JSON file
    with open("config.json", "r") as config_file:
        json_config = json.load(config_file)
    try:
        covid_api = json_config["covid_api"]
        filter_param = [covid_api["areaCode"]]
    except KeyError as excep:
        logging.error("area code or covid dictionary is missing in JSON file " + excep)
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByPublishDate": "newDeaths28DaysByPublishDate",
        "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate"
    }
    #Getting the JSON file of user-defined parameters
    api = Cov19API(filters=filter_param, structure=cases_and_deaths, latest_by="date")
    covid_json = api.get_json()
    covid_data = covid_json['data']
    #Creates a user friendly version of the covid info in the form of a string
    covid_notification = {"title" : "COVID Update" , "content": "There are " + str(covid_data[0]['newCasesByPublishDate'])
                        + " new cases today in " + covid_data[0]["areaName"] + ". A total of " + str(covid_data[0]['cumCasesByPublishDate']) +
                        " cases. There has been " + str(
            covid_data[0]["newDeaths28DaysByPublishDate"]) + " new deaths. A total of " + str(
            covid_data[0]["cumDeaths28DaysByPublishDate"]) + " deaths."}
    #Checking if the covid notification isnt already in the list of current notifications
    if covid_notification not in global_variables.covid_notif:
        global_variables.covid_notif.append(covid_notification)
        global_variables.current_notifs.insert(1,covid_notification)
    return covid_notification
