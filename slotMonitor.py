# This program watches the state of the syringe slots.
# The inserted syringes press the switch, changing the state to high.
# A low signal indicates a removed syringe.
#
# Written by Chris Quartararo
# Last updated 11/13/2019
#


# Import the necessary packages
import RPi.GPIO as gpio
from time import sleep


# Configures the GPIO and the inputs using BCM numbering to retain functionality across models.
# Inputs are currently set up to GPIO pins 16, 20, and 21.
gpio.setmode(gpio.BCM)
inputPins = [16,20,21]
gpio.setup(inputPins, gpio.IN)



# Callback functions to run on edge detection
# Callbacks will be run on both rising and falling edges, polling determines the direction
# This method dynamically runs the respective method for when a button is pressed or released
def onEdgeDetection(pin):
	# Initializes self for attribute calling
	self = __import__(__name__)

	# Dynamically calls the correct method
	methodName = 'day'+str(pin)
	method = getattr(self, methodName)
	return method(pin)
# Method to adjust the status of the syringe given a day of the week (0-6)
def adjustSyringeStatus(pin, day):
	days = {0: "Sunday",
		1: "Monday",
		2: "Tuesday",
		3: "Wednesday",
		4: "Thursday",
		5: "Friday",
		6: "Saturday"}
	dayString = days.get(day)
	if gpio.input(pin):
		print("Changing status of pin " + dayString + " (pin " + str(pin) + ") to True")
		pinStatus[day] = 1
	else:
		print("Changing status of pin" + dayString + " (pin " + str(pin) + ") to False")
		pinStatus[day] = 0
# Day of the week methods. The GPIO pin numbers are appended to the end of each method
# Sunday
def day16(pin):
	adjustSyringeStatus(pin, 0)
# Monday
def day20(pin):
	adjustSyringeStatus(pin, 1)
# Tuesday
def day21(pin):
	adjustSyringeStatus(pin, 2)
# Wednesday
def day3(pin):
	adjustSyringeStatus(pin, 3)
# Thursday
def day4(pin):
	adjustSyringeStatus(pin, 4)
# Friday
def day5(pin):
	adjustSyringeStatus(pin, 5)
# Saturday
def day6(pin):
	adjustSyringeStatus(pin, 6)



# Creates a list with the status of each of the pins
# The list starts at 0 for Sunday and ends at 6 for Saturday
pinStatus = [0,0,0,0,0,0,0]


# Adds the events to the listener
for pin in inputPins:
	gpio.add_event_detect(pin, gpio.BOTH, onEdgeDetection)


# Main loop of the program to keep it alive
while(True):
	try:
		print(pinStatus)
		sleep(1)
	except KeyboardInterrupt:
		break


