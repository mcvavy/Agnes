import snowboydecoder
import sys
import signal
import os

import logging
import pkgutil
import agnespath
from mic import Mic as microphone

from player import Player
import speech_recognition as sr


class Initiator:

    def __init__(self):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules. Note that the order of brain.modules
        matters, as the Brain will cease execution on the first module
        that accepts a given input.

        Arguments:
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        """
        self.modules = self.get_modules()
        self._logger = logging.getLogger(__name__)

        self.player = Player()


    def record_audio(self, fname):
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

            self.query(transcribed_voice_to_text)

        except sr.UnknownValueError:
            self.player.say("I do not understand your request, could you repeat that please")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        os.remove(fname)
        # self.clearOutWaveFiles()

    def clearOutWaveFiles(self):
        try:
            directory_name = os.getcwd()
            wavefiles_to_delete = os.listdir(directory_name)

            for item in wavefiles_to_delete:
                if item.endswith(".wav"):
                    os.remove(os.path.join(directory_name, item))
        except OSError:
            print("Files maybe deleted but something went wrong")


    # @classmethod
    def get_modules(self):
        """
        Dynamically loads all the modules in the modules folder and sorts
        them by the PRIORITY key. If no PRIORITY is defined for a given
        module, a priority of 0 is assumed.
        """

        logger = logging.getLogger(__name__)
        locations = [agnespath.PLUGIN_PATH]
        logger.debug("Looking for modules in: %s",
                     ', '.join(["'%s'" % location for location in locations]))
        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except:
                logger.warning("Skipped module '%s' due to an error.", name,
                               exc_info=True)
            else:
                if hasattr(mod, 'WORDS'):
                    logger.debug("Found module '%s' with words: %r", name,
                                 mod.WORDS)
                    modules.append(mod)
                else:
                    logger.warning("Skipped module '%s' because it misses " +
                                   "the WORDS constant.", name)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                     else 0, reverse=True)
        return modules

    def query(self, text):

        """
        Passes user input to the appropriate module, testing it against
        each candidate module's isValid function.

        Arguments:
        text -- user input, typically speech, to be parsed by a module
        """
        for module in self.modules:
            if module.isValid(text):
                print("texts is valid::::", text)
                self._logger.debug("'%s' is a valid phrase for module " +
                                   "'%s'", text, module.__name__)
                try:
                    module.handle(text, self.player)
                except Exception:
                    self._logger.error('Failed to execute module',
                                       exc_info=True)
                    self.player.say("I'm sorry. I had some trouble with " +
                                 "that operation. Please try again later.")
                else:
                    self._logger.debug("Handling of phrase '%s' by " +
                                       "module '%s' completed", text,
                                       module.__name__)
                finally:
                    return
        self._logger.debug("No module was able to handle any of these " +
                           "phrases: %r", text)

    def pause_music(self):
        self.player.pause_music()


if __name__ == '__main__':

    interrupted = False

    print("*******************************************************")
    print("*    Agnes - Your intelligent personal assistant      *")
    print("*         (c) 2019 Michael Oyibo                      *")
    print("*******************************************************")


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

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5) #befoire 0.38
    print('Listening... Press Ctrl+C to exit')

    initiator = Initiator()

    # main loop
    detector.start(detected_callback=snowboydecoder.play_audio_file,
                   audio_recorder_callback=initiator.record_audio,
                   interrupt_check=interrupt_callback,
                   pause_music_player=initiator.pause_music,
                   sleep_time=0.01)

    detector.terminate()