#
# This program watches the status of the PowerBoost 1000C providing power to the Raspberry Pi.
#
# The main loop watches for a falling edge on the USB pin indicating the device has been unplugged.
# The designated person is notified via email when the falling edge is detected. An email will be
# sent to the designated when a rising edge is detected indicating it has been plugged back in.
#
# Secondarily this program will watch the low_bat pin on the PowerBoost and gracefully shut down
# if a low charge is detected.
#


# Import the necessary modules
import RPi.GPIO as gpio
import emailStatus as email
import config
from time import sleep

# Callback functions for when edge is detected
def edgeDetected(channel):

	# Pause for 1 second to let the pin finish falling before polling for status
	sleep(1)

	# Poll for status to determine which edge was detected
	if gpio.input(channel):  # Rising edge (from 0 to 1)
		print("Rising edge detected: pin " + str(channel) + " <" + str(gpio.input(channel)) + ">")
	else:  # Falling edge (from 1 to 0)
		print("Falling edge detected: pin "+ str(channel) + " <" + str(gpio.input(channel)) + ">")

## Set up the GPIO pins
gpio.setmode(gpio.BCM)  # Using Broadcom numbering
# USB pin detects wall power. Needs to be pulled down when not plugged in.
gpio.setup(config.boostUSB, gpio.IN, pull_up_down = gpio.PUD_DOWN)
# LBO detects low battery. Needs to be pulled up or pi will artificially trigger LBO.
gpio.setup(config.boostLBO, gpio.IN, pull_up_down = gpio.PUD_UP)
# Add the edge detection on this channel. Bouncetime is set to 3s
gpio.add_event_detect(config.boostUSB, gpio.BOTH, callback = edgeDetected, bouncetime = 3000) # 3s bounce time
gpio.add_event_detect(config.boostLBO, gpio.FALLING, callback = edgeDetected, bouncetime = 30000) # 30s bounce time

# Main loop
try:
	# Pause for 5 seconds and print paused so we can se how the loop is progressing
	while(True):
		print("Paused")
		sleep(5)
except KeyboardInterrupt:
	pass
finally:
	gpio.cleanup()  # Closes the inputs for the GPIO
