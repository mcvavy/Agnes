import speech_recognition as sr
from player import Player



class Mic:
    def __init__(self):
        self.player = Player()

    def record_audio(self, fname, audio_rec_end = None):
        r = sr.Recognizer()
        with sr.AudioFile(fname) as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)  # read the entire audio file

        audio_rec_end(fname)

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            transcribed_voice_to_text = r.recognize_google(audio, language="en-GB")

            return transcribed_voice_to_text

        except sr.UnknownValueError:
            self.say("I do not understand your request, could you repeat that please")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def say(self, text):
        self.player.say(text)