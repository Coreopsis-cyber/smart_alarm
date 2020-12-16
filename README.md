# Smart Alarm

This code creates a smart alarm with a user interface in the browser. It gives the user the ability to schedule and cancel alarms by filling out a form on the html template as well as recieve top news headlines, the local weather and regional covid statistics in the form of notifications should they be requested. 

# Prerequisites 

This code functions on python 3.7 or above to download this onto your machine got to "https://www.python.org/downloads/".

To run the code, you will need a web browser google chrome preferably, you can download it here "https://www.google.com/chrome/". Other web browsers (e.g safari) may not exectute as intended.

For this code to function it requires an API key for both the weather and news modules. This can be aquired by going on "https://newsapi.org/" and "https://openweathermap.org/api" and signing up for a free API key. this should then be added the the configuration file called "config.json" in-between the quotation marks for the appropriate key. In that file you may also customise your location for the weather api by changing the city to the city you are currently in. You will also need an area code to get covid 19 data from a specific region in the UK. Use "https://findthatpostcode.uk/areatypes/rgn.html" to find the one for your area.

It also requires certain modules to be installed:
To do this open up the command line (search command line in your apps if you have difficulty finding it) and manually install them one at a time by copying each line seperately into the command line and pressing enter after each one.
```sh
$ pip3 install flask
$ pip3 install pyttsx3
$ pip3 install uk_covid19
$ pip3 install requests
```

As the API calls are in real time therefore internet connection is required for this application.

# Getting started

Through the command line navigate to the CA3 directory (if you are finding that difficult go to "https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/command-line-101/") which is the program folder.  

Copy the following line into the command line and press enter:

$ python3 main.py

You should see this message appear:
```sh
Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 ```
 After this, go to web browser (chrome preferably) and enter in the search bar at the top:
 127.0.0.1:5000
 
 On the left will display a list of alarms that are set and have yet to go off. On the right it will display a list of notifications for COVID, the weather and the news. Each element of both lists will have a `X` button on them to remove the element from the list. In the centre contains a form to set an alarm.
 Press the calender in the corner and set a date and time for the alarm, then add the name of your alarm in the bar with the words update label. The two check boxes allow you to choose if there's a news and weather briefing in the verbal announcement of the alarm. You can pick one or the other or both. All alarms announce COVID data as well as the name of the alarm.
 
 There may be a delay on the alarms of up to a minute as it refreshes every 60 seconds. 
 
 
 # Developer Information
 
 This program contains these files:

-Template folder which contains the HTML template for the program.

-Static folder containing images.

-config.json is a persistent file containing private and important data which can change the workings of the      program.

-sys.log logs all events performed by the application including every time the page refreshes.

-covid.py is the module for retrieving and formatting the covid data from the covid 19 API.

-weather.py is the module for retrieving and formatting the weather data from the weather API.

-news.py is the module for retrieving and formatting the top news headlines from the news API.

-global_variables.py contains the variables used by all other modules together

-main.py is the module in which the code can be run from, it is the module that directly deals with updating the interface e.g., setting and deleting alarms
 
# Updates

For the latest version of this code click the link to access the GitHub repository with the latest updated code. 
"[https://github.com/umennear/smart_alarm]"


# Licence

MIT License

Copyright (c) 2020 Ursula Mennear

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


