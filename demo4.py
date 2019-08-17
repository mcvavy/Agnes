import snowboydecoder
import sys
import signal
import speech_recognition as sr
import os
import re
import asyncio

from gtts import gTTS
from io import BytesIO
from pygame import mixer as Player

import pygame



# Music Player Setup
from mpyg321.mpyg321 import MPyg321Player
from time import sleep
musicPlayer = MPyg321Player()
#___________________


from datetime import datetime

from wit import Wit
witClient = Wit("JTUTA7EED6JP2VNJPJJOQKT3P7UPQ2HK")

import json

import random

import pyowm
owm = pyowm.OWM('dcac096e8c94a58b502991795e61f6d4')  # You MUST provide a valid API key

#Music setup
music_file_path = "./Music"
# music_files = filter(lambda filename: filename.split(".")[-1] == "mp3", os.listdir(music_file_path))
music_files = list(filter(lambda f: f.endswith('.mp3'), os.listdir(music_file_path)))
# print(json.dumps(music_files))

music_index = 0



Player.init()

music_position = 0
start = 0

musicPaused = False

jokes = ["Hey there how are you? Can I help?", "I am Echelon, how can I help you today", "It's an amazing day isn't it?", "It's my pleasure to help. Please ask me anything", "Good day you !"]

"""
This demo file shows you how to use the new_message_callback to interact with
the recorded audio after a keyword is spoken. It uses the speech recognition
library in order to convert the recorded audio into text.

Information on installing the speech recognition library can be found at:
https://pypi.python.org/pypi/SpeechRecognition/
"""


interrupted = False


def audioRecorderCallback(fname):
    print("converting audio to text")
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)  # read the entire audio file

    snowboydecoder.play_audio_file_end()
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        transcribed_voice_to_text = r.recognize_google(audio, language="en-GB")
        # print(r.recognize_google(audio))

        try:
            response = witClient.message(transcribed_voice_to_text)
            # witClient.interactive()
        except:
            Say("Something went wrong with the request")

        print(json.dumps(response, indent=2))


        # mp3_buffer = BytesIO()
        # tts = gTTS(transcribed_voice_to_text,lang='en')
        # tts.write_to_fp(mp3_buffer)
        # mp3_buffer.seek(0)
        # Player.music.load(mp3_buffer)
        # Player.music.play()

        try:

            if 'intent' in response['entities']:
                processIntent(response['entities']['intent'][0]['value'], response)

            if 'next' in response['entities']:
                processIntent('next_song', response)

            if 'stop' in response['entities']:
                processIntent('stop_song', response)

            if 'datetime' in response['entities']:
                processIntent('datetime', response)

        except KeyError:
            Say(
                "Sorry I cannot process your request, I am still very young, but am learning very quickly Trust me I am trying.")

    except sr.UnknownValueError:
        Say("I do not understand your request, could you repeat that please")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    os.remove(fname)
    # clearOutWaveFiles()

def clearOutWaveFiles():
    try:
        directory_name = os.getcwd()
        wavefiles_to_delete = os.listdir(directory_name)

        for item in wavefiles_to_delete:
            if item.endswith(".wav"):
                os.remove(os.path.join(directory_name, item))
    except OSError:
        print("Files maybe deleted but something went wrong")

def play_music():
    print("Playing music now.......")
    global music_index
    music_index += 1

    Player.music.load("./Music/{0}".format(music_files[music_index]))
    # Player.music.set_volume(0.4)
    Player.music.play()

    # musicPlayer.play_song("./Music/{0}".format(music_files[music_index]))


def resume_music():
    global start
    global music_position
    start = start + music_position/1000.0

    if musicPaused:
        global musicPaused
        musicPaused = False

        Player.music.load("./Music/{0}".format(music_files[music_index]))
        Player.music.play(-1, start)
    #
    # musicPlayer.resume()

def pause_music():
    if Player.music.get_busy():
        print("Pausing the music....")
        global music_position
        # player.music.fadeout(3/1000)
        Player.music.pause()
        music_position = Player.music.get_pos()
        print("Music position is {0}".format(music_position))
        global musicPaused
        musicPaused = True
    # musicPlayer.pause()

def play_next():
    global music_index
    music_index += 1

    Player.music.load("./Music/{0}".format(music_files[music_index]))
    # Player.music.set_volume(0.5)
    Player.music.play()
    # musicPlayer.stop()
    # musicPlayer.play_song("./Music/{0}".format(music_files[music_index]))

def stop_music():
    # Player.music.stop()
    musicPlayer.stop()

def Say(text):
    SONG_END = pygame.USEREVENT + 1

    tts = gTTS(text, lang='en')

    sf = BytesIO()
    tts.write_to_fp(sf)
    sf.seek(0)
    Player.music.load(sf)
    Player.music.play()
    Player.music.set_endevent(SONG_END)
    # Player.music.set_volume(0.4)

    while True:
        if Player.music.get_endevent() == SONG_END and not Player.music.get_busy():
            print("Say has finally ended.......Yippi")
            resume_music()
            break


def processIntent(intent, response):
    if intent == 'get_temp':
        if 'resolved' in response['entities']['location'][0]:
            Say('I have found more than one location for {0}, please be more specific like {0} UK or London UK'.format(
                response['entities']['location'][0]['value']))
        else:
            w = fetch_Temperature(re.sub("\s+", ",", response['entities']['location'][0]['value'].strip()))
            Say("The temperature is {0} degree celcius".format(w.get_temperature('celsius')['temp']))

    if intent == 'get_forecast':
        if 'resolved' in response['entities']['location'][0]:
            Say('I have found more than one location for {0}, please be more specific like {0} UK or London UK'.format(
                response['entities']['location'][0]['value']))
        else:
            w = fetch_Temperature(re.sub("\s+", ",", response['entities']['location'][0]['value'].strip()))
            weatherObject = w.get_temperature('celsius')
            Say(
                "Today's forecast are as follows. Wind speed is {0} miles per hour, humidity is {1}, and temperature is {2} degrees with a low of {3} degrees and a high of {4} degrees. Do have a wonderful day".format(
                    w.get_wind()['speed'], w.get_humidity(), weatherObject['temp'], weatherObject['temp_min'],
                    weatherObject['temp_max']))

    if intent == 'get_creator':
        Say('Well my name is Agnes. I am a young intelligent personal assistant created by Michael Oyibo.')

    if intent == 'get_song':
        play_music()

    if intent == 'next_song':
        play_next()

    if intent == 'get_stop':
        stop_music()

    if intent == 'get_time' or intent == 'datetime':
        now = datetime.now()
        Say("The time is {0}".format(now.strftime("%-I:%M %p")))

    if intent == 'greet_morning':
        Say("Good morning to you. I hope you are good")

    if intent == 'greetings':
        Say("I am very well thank you. Thanks for asking.")

    # resume_music()

def fetch_Temperature(location):
    observation = owm.weather_at_place(location)
    return observation.get_weather()

def detectedCallback():
  print('recording audio...', end='', flush=True)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.38)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=snowboydecoder.play_audio_file,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               pause_music_player=pause_music,
               sleep_time=0.01)

detector.terminate()




