#
# This script will shutdown the computer gracefully if called
#


# Import the necessary modules
from subprocess import call

# Shutdown method
def shutdown():
	call("sudo shutdown --poweroff", shell = True)

# If this script is called directly then call the shutdown routine
if __name__ == "__main__":
	shutdown()


