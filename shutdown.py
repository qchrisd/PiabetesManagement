#
# This script will shutdown the computer gracefully if called
#


# Import the necessary modules
from subprocess import call

# Shutdown method
def shutdown():
	call("sudo shutdown now --poweroff", shell = True)


if __name__ == "__main__":
	shutdown()


