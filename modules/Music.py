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


    if bool(re.search(r'\bshuffle\b', text, re.IGNORECASE)):
        music_player.play_shuffle()

    elif bool(re.search(r'\bnext\b', text, re.IGNORECASE)) or bool(re.search(r'\bskip\b', text, re.IGNORECASE)):
        music_player.play_next()
    else:
        music_player.play_music()


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bmusic\b', text, re.IGNORECASE)) or bool(re.search(r'\bsong\b', text, re.IGNORECASE))
