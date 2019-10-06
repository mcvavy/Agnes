# -*- coding: utf-8-*-
import re
import RPi.GPIO as GPIO
from nrf.sig import Radio

GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

WORDS = ["LIGHT"]


def handle(text, mic):
    radio = Radio(mic, text)
    radio.sendSignal()

def isValid(text):
    """
        Returns True if input is related to the time.
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\blight\b', text, re.IGNORECASE))