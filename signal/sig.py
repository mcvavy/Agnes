import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev

class Radio:
    def __init__(self, mic, text):
        self.text = text
        self.mic = mic
        self.pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio.begin(0, 25)
        self.radio.setRetries(15, 15)
        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x60)
        self.radio.setDataRate(NRF24.BR_2MBPS)
        self.radio.setPALevel(NRF24.PA_MIN)
        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()

        self.radio.openWritingPipe(self.pipes[1])
        self.radio.openReadingPipe(1, self.pipes[0])
        self.radio.printDetails()

        self.ackPL = [1]

    def receiveData(self):
        print("Ready to receive data.")
        self.radio.startListening()
        self.pipe = [0]
        while not self.radio.available(self.pipe):
            time.sleep(1 / 100)
        receivedMessage = []
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())

        print("Translating the receivedMessage to unicode characters...")
        string = ""
        for n in receivedMessage:
            # We want to only decode standard symbols/alphabet/numerals
            # Based off unicode standards, our encoding method
            if (n >= 32 and n <= 126):
                string += chr(n)
        print("Our sensor sent us: {}".format(string))
        self.mic.say(string)
        self.radio.stopListening()

    def sendSignal(self):
        message = []
        message = list(self.text)

        # send a packet to receiver
        self.radio.write(message)
        print("Sent: {}".format(message))

        # did it return with a payload?
        if self.radio.isAckPayloadAvailable():
            pl_buffer = []
            self.radio.read(pl_buffer, self.radio.getDynamicPayloadSize())
            print(pl_buffer)
            print("Translating the acknowledgement to unicode characters...")
            string = ""
            for n in pl_buffer:
                # We want to only decode standard symbols/alphabet/numerals
                # Based off unicode standards, our encoding method
                if (n >= 32 and n <= 126):
                    string += chr(n)
            print(string)
            # So our command was received and acknowledged. We should
            # setup ourselves to receive what that temperature was.
            self.receiveData()
        else:
            print("No received acknowledgement.")
        time.sleep(0.5)