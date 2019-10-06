import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

import re

GPIO.setmode(GPIO.BCM)
gpioList = [26, 19, 13, 0o6, 12, 16, 20, 21]

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 25)
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()

radio.startListening()


def getTemp():
    temp = 25
    return str(temp)


def sendData(ID, value):
    radio.stopListening()
    time.sleep(0.25)
    message = list(ID) + list(value)
    print("About to send the message.")
    radio.write(message)
    print("Sent the data.")
    radio.startListening()


def sendMaster(value):
    radio.stopListening()
    time.sleep(0.25)
    message = list(value)
    print("About to send the message.")
    radio.write(message)
    print("Sent the data.")
    radio.startListening()


def triggerLight(text):
    for i in gpioList:
        GPIO.setup(i, GPIO.OUT)
        # GPIO.output(i, GPIO.HIGH)

    if bool(re.search(r'\bbedroom\b', text, re.IGNORECASE)):
        try:

            if GPIO.input(26) == 1:
                print("This this: {0}".format(GPIO.input(26)))
                GPIO.output(26, GPIO.LOW)
                sendMaster("Bedroom light is on")
            else:
                GPIO.output(26, GPIO.HIGH)
                sendMaster("Bedroom light is off")

        except:
            print("An error occurred")
            GPIO.cleanup()

    if bool(re.search(r'\bkitchen\b', text, re.IGNORECASE)):
        try:

            if GPIO.input(21) == 1:
                print("This this: {0}".format(GPIO.input(26)))
                GPIO.output(21, GPIO.LOW)
                sendMaster("Kitchen light is on")
            else:
                GPIO.output(21, GPIO.HIGH)
                sendMaster("Kitchen light is off")

        except:
            print("An error occurred")
            GPIO.cleanup()

    if bool(re.search(r'\bliving\b', text, re.IGNORECASE)):
        try:

            if GPIO.input(20) == 1:
                print("This this: {0}".format(GPIO.input(26)))
                GPIO.output(20, GPIO.LOW)
                sendMaster("Living room light is on")
            else:
                GPIO.output(20, GPIO.HIGH)
                sendMaster("Living room light is off")

        except:
            print("An error occurred")
            GPIO.cleanup()


while True:
    ackPL = [1]
    radio.writeAckPayload(1, ackPL, len(ackPL))
    while not radio.available(0):
        time.sleep(1 / 100)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))

    print("Translating the receivedMessage into unicode characters...")
    string = ""
    for n in receivedMessage:
        # Decode into standard unicode set
        if (n >= 32 and n <= 126):
            string += chr(n)
    print(string)

    # We want to react to the command from the master.

    # Try trigger lights
    triggerLight(string)

    radio.writeAckPayload(1, ackPL, len(ackPL))
    print("Loaded payload reply of {}".format(ackPL))