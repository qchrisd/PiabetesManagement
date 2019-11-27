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

# Set up the GPIO pins
gpio.setmode(gpio.BCM)  # Using Broadcom numbering
gpio.setup(12, gpio.IN, pull_up_down = gpio.PUD_DOWN)  # Set up pin 12 as input with pull down resistor
gpio.setup(25, gpio.IN, pull_up_down = gpio.PUD_UP)  # Set up pin 25 as input with pull down resistor
# Add the edge detection on this channel. Bouncetime is set to 3s
gpio.add_event_detect(12, gpio.BOTH, callback = edgeDetected, bouncetime = 3000)
gpio.add_event_detect(25, gpio.FALLING, callback = edgeDetected, bouncetime = 3000)

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
