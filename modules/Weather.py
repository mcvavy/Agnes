import re
import json

import pyowm
owm = pyowm.OWM('dcac096e8c94a58b502991795e61f6d4')  # You MUST provide a valid API key

from wit import Wit
witClient = Wit("JTUTA7EED6JP2VNJPJJOQKT3P7UPQ2HK")

WORDS = ["WEATHER, FORECAST, TEMPERATURE, HOT, COLD, WARM"]


def handle(text, mic):
    try:
        response = witClient.message(text)
    except:
        mic.say("Something went wrong with the request")

    print(json.dumps(response, indent=2))

    try:

        if 'intent' in response['entities']:
            processIntent(response['entities']['intent'][0]['value'], response, mic)

    except KeyError:
        mic.say("Sorry I cannot process your request, I am still very young, but am learning very quickly Trust me I am trying.")

def isValid(text):

    return bool(re.search(r'\bweather\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\btemperature\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bcold\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bwarm\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\brain\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bhot\b', text, re.IGNORECASE))

def processIntent(intent, response, mic):
    if intent == 'get_temp':
        if 'resolved' in response['entities']['location'][0]:
            mic.say('I have found more than one location for {0}, please be more specific like {0} UK or London UK'.format(
                response['entities']['location'][0]['value']))
        else:
            w = fetch_Temperature(re.sub("\s+", ",", response['entities']['location'][0]['value'].strip()))
            mic.say("The temperature is {0} degree celcius".format(w.get_temperature('celsius')['temp']))

    if intent == 'get_forecast':
        if 'resolved' in response['entities']['location'][0]:
            mic.say('I have found more than one location for {0}, please be more specific like {0} UK or London UK'.format(
                response['entities']['location'][0]['value']))
        else:
            w = fetch_Temperature(re.sub("\s+", ",", response['entities']['location'][0]['value'].strip()))
            weatherObject = w.get_temperature('celsius')
            mic.say(
                "Today's forecast are as follows. Wind speed is {0} miles per hour, humidity is {1}, and temperature is {2} degrees with a low of {3} degrees and a high of {4} degrees. Do have a wonderful day".format(
                    w.get_wind()['speed'], w.get_humidity(), weatherObject['temp'], weatherObject['temp_min'],
                    weatherObject['temp_max']))

def fetch_Temperature(location):
    observation = owm.weather_at_place(location)
    return observation.get_weather()
