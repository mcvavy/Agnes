import re

# from player import Player
# mic = Player()

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
        mic.play_shuffle()
    elif bool(re.search(r'\bnext\b', text, re.IGNORECASE)) or bool(re.search(r'\bskip\b', text, re.IGNORECASE)):
        mic.play_next()
    elif bool(re.search(r'\bpause\b', text, re.IGNORECASE)):
        mic.pause_music()
    elif bool(re.search(r'\bstop\b', text, re.IGNORECASE)):
        mic.stop_music()
    elif bool(re.search(r'\bvolume\b', text, re.IGNORECASE)):
        if bool(re.search(r'\bhigh\b', text, re.IGNORECASE)):
            mic.set_volume("high")
        if bool(re.search(r'\blow\b', text, re.IGNORECASE)):
            mic.set_volume("low")
        if bool(re.search(r'\bmedium\b', text, re.IGNORECASE)):
            mic.set_volume("medium")

    else:
        mic.play_music()


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bmusic\b', text, re.IGNORECASE)) or bool(re.search(r'\bsong\b', text, re.IGNORECASE))
