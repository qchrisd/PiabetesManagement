#
# This program watches the state of the syringe slots.
# The inserted syringes press the switch, changing the state to high.
# A low signal indicates a removed syringe.
#
# Written by Chris Quartararo
# Last updated 11/13/2019
#


# Import the necessary packages
import RPi.GPIO as gpio
import time
# Import local modules
import log
import emailStatus
import shutdown
from config import *


## Create some variables
# Creates a list of input pins in a list
inputs = [sun, mon, tue, wed, thu, fri, sat]
# Creates a list of the days of the week
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
# Creates a dictionary where each day is keyed to the corresponding input pin
inputDays = dict(zip(inputs, days))


## Configures the GPIO and the inputs using BCM numbering to retain functionality across models.
gpio.setmode(gpio.BCM)
# Sets up the input pins with pull down resistors
gpio.setup(inputs, gpio.IN, pull_up_down=gpio.PUD_DOWN)
# Sets up the power management inputs
gpio.setup(boostUSB, gpio.IN, pull_up_down=gpio.PUD_DOWN)  # Wall power input
gpio.setup(boostLBO, gpio.IN, pull_up_down=gpio.PUD_UP)  # low battery

## Callback functions to run on edge detection
# Callbacks will be run on both rising and falling edges, polling determines the direction
# This method dynamically runs the respective method for when a button is pressed or released
def photoEdgeDetected(pin):
	# Initializes self for attribute calling
	self = __import__(__name__)

	# Dynamically calls the correct method
	methodName = 'change'+inputDays.get(pin)
	method = getattr(self, methodName)
	return method(pin)
# Method to adjust the status of the syringe given a day of the week (0-6)
def adjustSyringeStatus(pin):
	dayString = inputDays.get(pin)
	time.sleep(.2)
	# If the pin is high, the light reaches the phototransistor and the syringe is not in the holder
	if gpio.input(pin):
		emailStatus.sendEmail(emailStatus.formatEmail("Syringe Change Detected","{}'s syringe was just added to the holder.".format(dayString)))
		log.logMessage("{}'s syringe was just removed from the holder.".format(dayString))
		pinStatus[inputs.index(pin)] = 0
	# If the pin is low, the light is blocked and the syringe is in the holder
	else:
		emailStatus.sendEmail(emailStatus.formatEmail("Syringe Change Detected","{}'s syringe was just removed from the holder.".format(dayString)))
		log.logMessage("{}'s syringe was just added to the holder.".format(dayString))
		pinStatus[inputs.index(pin)] = 1
# Day of the week methods. The GPIO pin numbers are appended to the end of each method
# Sunday
def changeSunday(pin):
	adjustSyringeStatus(pin)
# Monday
def changeMonday(pin):
	adjustSyringeStatus(pin)
# Tuesday
def changeTuesday(pin):
	adjustSyringeStatus(pin)
# Wednesday
def changeWednesday(pin):
	adjustSyringeStatus(pin)
# Thursday
def changeThursday(pin):
	adjustSyringeStatus(pin)
# Friday
def changeFriday(pin):
	adjustSyringeStatus(pin)
# Saturday
def changeSaturday(pin):
	adjustSyringeStatus(pin)


## Power managment edge function
def powerEdgeDetected(pin):

	# Pause for 1 second to let the pin finish falling before polling
	time.sleep(1)

	# Shutdown the Raspberry Pi if the battery is low
	if pin == boostLBO and not gpio.input(pin):
		log.logMessage("Low battery detected. Shutting the raspberry pi down.")
		shutdown.shutdown()

	# Log messages if the wall power is unplugged and plugged back in
	elif pin == boostUSB:
		# Rising edge (just plugged in)
		if gpio.input(pin):
			log.logMessage("Device plugged in.")
			emailStatus.sendEmail(emailStatus.formatEmail("Device Plugged In","The syringe monitor has just been plugged into wall power."))
		# Falling edge (just unplugged
		else:
			log.logMessage("Device unplugged.")
			emailStatus.sendEmail(emailStatus.formatEmail("Device Unplugged","The syringe monitor has just been unplugged from wall power. There is roughly 1 hour of battery life before the device shuts down." ))


# Creates a list with the status of each of the pins
# The list starts at 0 for Sunday and ends at 6 for Saturday
pinStatus = [0,0,0,0,0,0,0]

# Adds the events to the listener
for pin in inputs:
	time.sleep(.1)
	pinStatus[inputs.index(pin)] = int(not gpio.input(pin))
	gpio.add_event_detect(pin, gpio.BOTH, photoEdgeDetected, bouncetime=3000)  # 3s bounce time
# Adds power management edge detection
gpio.add_event_detect(boostUSB, gpio.BOTH, powerEdgeDetected, bouncetime = 3000)  # 3s bounce time
gpio.add_event_detect(boostLBO, gpio.FALLING, powerEdgeDetected, bouncetime = 65000) # 65s bounce time

# Main loop of the program to keep it alive
while(True):
	try:
		print(pinStatus)
		time.sleep(2)
	except KeyboardInterrupt:
		break


