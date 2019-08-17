# -*- coding: utf-8-*-
from datetime import datetime
import re

from player import Player
music_player = Player()

WORDS = ["MUSIC"]


def handle(text, mic):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    music_player.play_music()


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bmusic\b', text, re.IGNORECASE))
