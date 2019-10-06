# -*- coding: utf-8-*-
import re
import RPi.GPIO as GPIO
from signal.sig import Radio

GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

WORDS = ["LIGHT"]


def handle(text, mic):
    radio = Radio(mic, text)
    radio.sendSignal()