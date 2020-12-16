"""
Retrieves current Top news stories from API "newsapi.org".
"""
import json
import logging
import requests
import global_variables
import flask
from flask import Markup


logging.basicConfig(filename='sys.log',encoding= 'utf-8', level=logging.DEBUG)

def get_headlines() -> list :
    """
        Gets top headlines for the news based on the perameters set in the config file,
        then formats the data for the annoucement and notifications.

        Uses an API to get news headlines for a specified country. The headlines are then
        applied to a dictionary with keys title and content: the title contains the headline
        and the content contains a brief discription of the article.
        This is then added to a list of current notifications to be shown or announced

        Local variables:
        news_list = A list containing current top headlines
        Global variables:
        old_notif = a list (of dictionaries) containing previous notifications (news, weather and
        COVID)
        current_notif = a list (of dictionaries) containing current notifications (news, weather
         and COVID)

         Returns:
         a list of dictionaires containing news headlines and descriptions

    """
    news_list =[]
    base_url = 'http://newsapi.org/v2/top-headlines?'
    #Getting country and API key from config file to construct url
    with open("config.json", "r") as config_file:
        api_config = json.load(config_file)
        news_config = api_config['news_api']
        api_key = news_config['API_key_news']
        country = news_config['country']
    #Creates a complete URL from user-defined components
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    if response.status_code == 200:
            articles = response.json()["articles"]
            for article in articles:
                check_news_list = [{'title': article["title"], "content": Markup("<a href=" + article["url"] + ">" + article["url"] + "<a>")}]
                if check_news_list not in global_variables.old_notifs:
                    news_list.append({'title': article["title"], "content": article["description"]})
                    logging.info (article["title"] + " has been added to the list of notifications.")
                    global_variables.current_notifs.append({'title': article["title"], "content": Markup("<a href=" + article["url"] + ">"+ article["url"] + "<a>")})
                    global_variables.old_notifs.append({'title': article["title"], "content": Markup("<a href=" + article["url"] + ">"+ article["url"] + "<a>")})
    return news_list
