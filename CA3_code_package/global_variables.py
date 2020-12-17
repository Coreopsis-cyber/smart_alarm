"""
    Contains all of the global variables accessed by other modules

    alarms_list = has all the alarms that have been set up by the user and
                  haven't been set off yet

    current_notifs = has all the notifications being displayed in the notification column

    old_notifs = has notifications that were removed from current_notifs automatically or by
                 the user to make sure they are not repeated

    covid_notif = has all of the covid related updates displayed as notifications

    old_weather_notifs = has all the weather related updates that have been displayed as
                         notifications

"""

alarms_list = []
current_notifs = []
old_notifs = []
covid_notif = []
old_weather_notifs = []
