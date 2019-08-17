# -*- coding: utf-8-*-
from datetime import datetime
import re

WORDS = ["TIME"]


def handle(text, mic):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    now = datetime.now()
    mic.say("The time is {0}".format(now.strftime("%-I:%M %p")))


def isValid(text):

    print("Text recieved in handler is :::", text)
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\btime\b', text, re.IGNORECASE))
