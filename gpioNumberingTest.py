# Import dependencies
import RPi.GPIO as gpio

# Set up GPIO
gpio.setmode(gpio.BCM)

# Set up GPIO channels for the 3 buttons
gpio.setup([21,20,16], gpio.IN)


# Callback functions
def buttonPressBot(channel):
	if gpio.input(channel):
		print("Bottom button has been pressed")
	else:
		print("Bottom button has released")

def buttonPressMid(channel):
	if gpio.input(channel):
		print("Middle button has been pressed")
	else:
		print("Middle button has released")

def buttonPressTop(channel):
	if gpio.input(channel):
		print("Top button has been pressed")
	else:
		print("Top button has released")


# Adds a rising and falling edge for each button
gpio.add_event_detect(21, gpio.BOTH, callback = buttonPressBot)
gpio.add_event_detect(20, gpio.BOTH, callback = buttonPressMid)
gpio.add_event_detect(16, gpio.BOTH, callback = buttonPressTop)

keepGoing = 1
while(keepGoing):
	if gpio.event_detected(21):
		print("event detected")
	keepGoing = input()
#	gpio.event_detected(20)
#	gpio.event_detected(16)

#gpio.cleanup()
