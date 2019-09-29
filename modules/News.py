# -*- coding: utf-8-*-
import re
import requests
import json

from pygame import mixer as sound_player
import pygame

WORDS = ["NEWS"]


def handle(text, mic):
    #"Could not request results from Google Speech Recognition service; {0}".format(e)
    source = ""
    if bool(re.search(r'\bbbc\b', text, re.IGNORECASE)):
        source = "bbc-news"
    elif bool(re.search(r'\bcnn\b', text, re.IGNORECASE)):
        source = "cnn"
    else:
        source = "mirror"

    url = "https://newsapi.org/v2/top-headlines?" \
          "sources={0}" \
          "&sortBy=popularity" \
          "&apiKey=27033d1a7eea422d9c985a21736d4249".format(source)
    print("The request URL is: {0}".format(url))


    response = requests.get(url)
    response_data = response.json()

    # print(response_data["articles"])

    # mic.say(response_data["articles"][0]["title"])
    counter = 1
    for x in response_data["articles"]:
        mic.say("{0}. {1}".format(counter, x["title"]))
        counter = counter + 1
        print("%s" % (x["title"]))

    SONG_END = pygame.USEREVENT + 1

    while True:
        if sound_player.music.get_endevent() == SONG_END:
            if mic.musicPaused:
                mic.resume_music()
                break



def isValid(text):
    """
        Returns True if input is related to the time.
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bnews\b', text, re.IGNORECASE))