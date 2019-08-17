import os

from gtts import gTTS
from io import BytesIO

from pygame import mixer as sound_player
import pygame

class Player:
    def __init__(self):
        self._music_file_path = "./Music"
        self.music_files = list(filter(lambda f: f.endswith('.mp3'), os.listdir(self._music_file_path)))
        self.music_index = 0
        sound_player.init()

        self.music_position = 0
        self.start = 0

        self.musicPaused = False

    def say(self, text):
        SONG_END = pygame.USEREVENT + 1

        tts = gTTS(text, lang='en')

        sf = BytesIO()
        tts.write_to_fp(sf)
        sf.seek(0)
        sound_player.music.load(sf)
        sound_player.music.play()
        sound_player.music.set_endevent(SONG_END)
        # Player.music.set_volume(0.4)

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(100)

        while True:
            if sound_player.music.get_endevent() == SONG_END:
                self.resume_music()
                break

    def play_music(self):
        print("Playing music now.......")
        self.music_index += 1

        sound_player.music.load("./Music/{0}".format(self.music_files[self.music_index]))
        sound_player.music.play()


    def resume_music(self):

        self.start = self.start + self.music_position/1000.0

        if self.musicPaused:
            print("Resuming music...")
            self.musicPaused = False

            sound_player.music.load("./Music/{0}".format(self.music_files[self.music_index]))
            sound_player.music.play(-1, self.start)

    def pause_music(self):
        if sound_player.music.get_busy():
            print("Pausing the music....")
            sound_player.music.pause()
            self.music_position = sound_player.music.get_pos()
            print("Music position is {0}".format(self.music_position))
            self.musicPaused = True


    def play_next(self):
        self.music_index += 1

        sound_player.music.load("./Music/{0}".format(self.music_files[self.music_index]))
        sound_player.music.play()


    def stop_music(self):
        sound_player.music.stop()