# import re
# import RPi.GPIO as GPIO
# from signal.sig import Radio
#
# GPIO.setmode(GPIO.BCM)
# # GPIO.setwarnings(False)
#
# WORDS = ["LIGHT"]
#
#
# gpioList = [26, 19, 13, 0o6, 12, 16, 20, 21]
#
#     for i in gpioList:
#         GPIO.setup(i, GPIO.OUT)
#         # GPIO.output(i, GPIO.HIGH)
#
#     if bool(re.search(r'\bbedroom\b', text, re.IGNORECASE)):
#         try:
#
#             if GPIO.input(26) == 1:
#                 print("This this: {0}".format(GPIO.input(26)))
#                 GPIO.output(26, GPIO.LOW)
#                 mic.say("Bedroom light is on")
#             else:
#                 GPIO.output(26, GPIO.HIGH)
#                 mic.say("Bedroom light is off")
#
#         except:
#             print("An error occurred")
#             GPIO.cleanup()
#
#     if bool(re.search(r'\bkitchen\b', text, re.IGNORECASE)):
#         try:
#
#             if GPIO.input(21) == 1:
#                 print("This this: {0}".format(GPIO.input(26)))
#                 GPIO.output(21, GPIO.LOW)
#                 mic.say("Kitchen light is on")
#             else:
#                 GPIO.output(21, GPIO.HIGH)
#                 mic.say("Kitchen light is off")
#
#         except:
#             print("An error occurred")
#             GPIO.cleanup()
#
#     if bool(re.search(r'\bliving\b', text, re.IGNORECASE)):
#         try:
#
#             if GPIO.input(20) == 1:
#                 print("This this: {0}".format(GPIO.input(26)))
#                 GPIO.output(20, GPIO.LOW)
#                 mic.say("Living room light is on")
#             else:
#                 GPIO.output(20, GPIO.HIGH)
#                 mic.say("Living room light is off")
#
#         except:
#             print("An error occurred")
#             GPIO.cleanup()
#
# def isValid(text):
#     """
#         Returns True if input is related to the time.
#         Arguments:
#         text -- user-input, typically transcribed speech
#     """
#     return bool(re.search(r'\blight\b', text, re.IGNORECASE))