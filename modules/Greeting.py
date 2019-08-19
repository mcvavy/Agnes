import random
import re

WORDS = ["Greeting"]


def handle(text, mic):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    message = ""

    if bool(re.search(r'\bmorning\b', text, re.IGNORECASE)):
        message = "Good morning to you"
    elif bool(re.search(r'\bafternoon\b', text, re.IGNORECASE)):
        message = "Good afternoon to you"
    elif bool(re.search(r'\bevening\b', text, re.IGNORECASE)):
        message = "Good evening to you"
    elif bool(re.search(r'\bnight\b', text, re.IGNORECASE)):
        message = "Good night"
    else:
        message = "Hello there, how are you?"

    mic.say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bmorning\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bafternoon\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bevening\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bhi\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bhello\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bhey\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bwhat\'s up\b', text, re.IGNORECASE)) or \
           bool(re.search(r'\bnight\b', text, re.IGNORECASE))
