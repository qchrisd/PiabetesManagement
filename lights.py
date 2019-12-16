'''
This module runs the LED lights that will power the photointerrupters.

This device utilizes the Neopixels by Adafruit and the adafruit circtui python library to run them.
The neopixels must be controlled from GPIO pins 10,12, 18, or 21 due to hardware limitations when
controlling Pulse Width Modulation (PWM)

Last updated 12-16-2019

'''

# Import dependent packages
import config
import adafruit_circuitpython_neopixel as neopixel
import board

# Create the string of pixels
pixels = neopixel.Neopixels(config.lightPin, 7)  # 7 lights, one for each day of the week
pixels.fill(config.colors)


