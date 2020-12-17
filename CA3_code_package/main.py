"""
    Main module controlling functionalitly for the program.
"""

from CA3_code_package.news import get_headlines
from CA3_code_package.weather import get_weather
from CA3_code_package.covid import get_covid_info
from CA3_code_package.tests import testing
from CA3_code_package import global_variables

from flask import Flask
from flask import request
from flask import render_template
from datetime import datetime
from requests import get
import pyttsx3
import time
import sched
import logging


s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
engine = pyttsx3.init()
logging.basicConfig(filename='sys.log',encoding= 'utf-8', level=logging.DEBUG)
flask_logger = logging.getLogger('werkzeug')

@app.route("/")
def return_to_index() -> render_template:
    """
        This is called every 60 seconds or if the app manually refreshes for updating

        It updates the user interface by deleting alarms or notifications and automatically
        adding more news notifications. It also adds the covid and weather digest notifications at the
        top of the list.

    """
    manual_delete_notifications()
    manual_delete_alarm()
    get_weather()
    get_covid_info()
    if len(global_variables.current_notifs) <= 5:
        s.enter(60, 2, auto_add_notifications(), (get_headlines(),),)
    return render_template('template.html', title='Daily update',alarms=global_variables.alarms_list, notifications=global_variables.current_notifs, image ="download.png")

@app.route("/index", methods=['GET'])
def set_alarm() -> return_to_index:
    """
        Sets up alarm with requried infomation.

        Checks if new alarm is requested through the submit buttom on the interface. Then converts
        alarm time into seconds and gets the delay by minusing current time so the alarm knows
        when to be triggered.
        Sees whether the weather or news boxes have been checked to see if they need to be announced.

        Will create an alarm dictionary with all its infomation added to current alarm list.
    """
    s.run(blocking=False)
    if request.method == 'GET':
        content = request.args.get("alarm")
        title = request.args.get("two")
        if content is not None and title is not None:
            delay = 0
            news = bool(request.args.get("news"))
            weather = bool(request.args.get("weather"))
            formatted_time = datetime.strptime(content, '%Y-%m-%dT%H:%M')
            epoch_time = datetime.timestamp(formatted_time)
            delay = epoch_time - float(datetime.now().timestamp())
            alarm_dict = {"title": title,"content": str(formatted_time) + "\n" + " News report: " + str(news) + "\n" + " Weather report: " + str(weather), "news": news, "weather": weather, "epoch_time": epoch_time}
            s.enter(int(delay), 1, announce_alarm, (alarm_dict,))
            global_variables.alarms_list.append(alarm_dict)
            logging.info("An alarm " + title + " has been set for " + str(formatted_time))
        # Refreshes interface
    return return_to_index()

def announce_alarm(alarm_dict=None) -> None:
    """
        Uses text to speech module to announce alarm once triggered.

        alarm_dict = contains all the infomation pertaining to alarm, such as time, name and briefs

        It then determins the combination of announcements based on whether the news and the weather
        are true.
        Then it performs the announcement, adds the relevent notifications and removes the alarm
        from the list.

        It uses pyttsx3 module to announce the information.


    """
    if alarm_dict is None:
        alarm_dict = {}
    # Check if pyttsx3 engine is operating
    try:
        engine.endLoop()
    except:
        pass
    # Condition to check that alarm hasn't been removed after event was scheduled
    if alarm_dict in global_variables.alarms_list:
        # Exception handling if there is no new news articles that haven't been read
        try:
            get_headlines()[0]
        except IndexError:
            print("error no more news")
            logging.warning('Could not get news in announcement as there are currently no new news')
            global_variables.alarms_list.remove(alarm_dict)
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " \
                                + get_covid_info()["content"]
            engine.say(full_announcement)
            engine.runAndWait()
            return
        # Forms message
        if alarm_dict["news"] and alarm_dict["weather"]:
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " + \
                                get_covid_info()["content"] + ".  " \
                                + get_weather()['content'] + ". " \
                                + "The latest news story is, " + \
                                get_headlines()[0]["title"]
            if get_weather() not in global_variables.current_notifs:
                global_variables.current_notifs.append(get_weather())
            global_variables.old_notifs.append(get_headlines())

        elif alarm_dict["news"] and not alarm_dict["weather"]:
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " + \
                                get_covid_info()[
                                    "content"] + ". " + "The latest news story is," + \
                                get_headlines()[0]["title"]
            global_variables.old_notifs.append(get_headlines())

        elif not alarm_dict["news"] and alarm_dict["weather"]:
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " \
                                + get_covid_info()["content"] + ". " \
                                + get_weather()['content']
            if get_weather() not in global_variables.current_notifs:
                global_variables.current_notifs.append(get_weather())

        elif not alarm_dict["news"] and not alarm_dict["weather"]:
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " \
                                + get_covid_info()["content"]
        else:
            logging.error("Undefined combination of briefs wanted")
            full_announcement = "Error"
        # Check if covid notification is not already in the notification list
        if get_covid_info() not in global_variables.current_notifs:
            global_variables.current_notifs.append(get_covid_info())
        # Using pyttsx3 to announce message
        engine.say(full_announcement)
        engine.runAndWait()
        global_variables.alarms_list.remove(alarm_dict)
        logging.info(" Announcement for alarm: "+ str(alarm_dict['title']) + " for " + str(alarm_dict['content']) +" has been sounded")
        logging.info("The alarm: " + str(alarm_dict["title"]) + " has been removed from alarm list")

def auto_add_notifications(news_list=None) -> None:
    """
        Automatically adds news headlines to the notifications list.

        Argument:
        news_list = dictionary contains a news story's headline an link to article. Function
        function checks if there is space in notification list, then the function triggers a scheduled
        even to automatically remove this article from the list after a time delay.

    """
    if news_list is None:
            news_list = []
    if len(global_variables.current_notifs) <= 5:
        for article in news_list:
            if article not in global_variables.old_notifs:
                global_variables.old_notifs.append(article)
                global_variables.current_notifs.append(article)
                logging.info("article: " + str(article['title']) + " has been automatically added to the notification list")
                s.enter(180, 2, auto_remove_notifications, (article,), )
                break

def auto_remove_notifications(article=None) -> None:
    """
        Removes a notifcation from the global variable current notification given as the argument "article"

        Argument:
        article = a dictionary containing a news headline and the link to the website.
        This function is called by auto_add_notifications which automatically adds a news
        story, it then deletes them after a given ammount of time. A scheduled even in
        auto_add_notifications that takes the argument of the headline to be removed, calls
        this function to remove it.

    """
    if article is None:
        article ={}
    if article in global_variables.current_notifs:
        global_variables.current_notifs.remove(article)
        logging.info(str(article['title']) + " has been automatically removed from the notification list")

def manual_delete_alarm() -> None:
    """
        Deleting an alarm when user clicks the X button to delete.
        This is called in return_to_index which will refresh the template in the case of the user pressing
        the delete button next to the alarm name as this will change the URL which will state the name
        of the alarm to be deleted. Once this function is called in the return_to_index function, it will
        check if an alarm name is in the URL and take this name and remove it's associated alarm from
        from the list
    """

    # Checks if alarm name is in the URL
    if request.args.get("alarm_item"):
        alarm_to_remove = request.args.get("alarm_item")
        for alarm in global_variables.alarms_list:
            # Checks if this alarm for the alarm name is in the current alarm to be sounded list
            if alarm["title"] == alarm_to_remove:
                global_variables.alarms_list.remove(alarm)
                logging.debug("article: "+ str(alarm_to_remove) +" has been manually removed from the notification list")

def manual_delete_notifications() -> None:
    """
        Deleting a notification when user clicks the X button to delete.
        This is called in return_to_index which will refresh the template in the case of the user pressing
        the delete button next to the notification name as this will change the URL which will state the
        name of the notification to be deleted. Once this function is called in the return_to_index
        function, it will check if a notification name is in the URL and take this name and remove
        it's associated notification from the list.
        It is similar to the manual_delete_alarm function.
    """
    # Checks if notification name is in the URL
    if request.args.get("notif"):
        notif_to_remove = request.args.get("notif")
        for notif in global_variables.current_notifs:
            # Iterate of notification list to check if the item is there in the list
            if notif["title"] == notif_to_remove:
                global_variables.current_notifs.remove(notif)
                global_variables.old_notifs.append(notif)
                logging.info("The notification "+ str(notif_to_remove) + " has been manually removed from notification list",)

if __name__ == "__main__":
    logging.info('system starting')
    try:
        testing.test_api()
    except AssertionError as message:
        print(message)
    app.run()
