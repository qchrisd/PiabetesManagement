#
# This file opens the log file, marks down the event, and gracefully closes the file.
#


# Import the necessary modules
import config
import time


# Opens the file and logs the event in the current time
def logMessage(message):
	# Formats the string to log
	logString = "{0}: {1}\n".format(time.ctime(), message)
	with open(config.logFilePath, 'a') as log:
		log.write(logString)


# If this is the file called, run the program
if __name__ == "__main__":
	logMessage("Logger run independently")
