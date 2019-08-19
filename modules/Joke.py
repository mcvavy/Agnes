import random
import re

import requests

WORDS = ["JOKE"]


def handle(text, mic):

    response = requests.get("https://geek-jokes.sameerkumar.website/api")
    mic.say(response.json())


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bjoke\b', text, re.IGNORECASE)) or bool(re.search(r'\blaugh\b', text, re.IGNORECASE))
