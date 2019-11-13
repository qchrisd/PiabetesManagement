
# Testing output and whatnot of the Raspberry Pi GPIO
#
# written by Chris Quartararo
# 11/12/2019
#
#

# Import the necessary libraries for things to work
import RPi.GPIO as gpio
from time import sleep

# Set up the GPIO with the BCM pin numbering system
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

# Set up the input channel
gpio.setup(18, gpio.IN)

# Set up the loop to display whether the input is high or low each second
count = 0
while(count < 100):
	print(gpio.input(18))
	sleep(1)
	count += 1

# Run some stats on how this input looks after 100 seconds
