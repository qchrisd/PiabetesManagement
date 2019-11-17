#
# This program sends an email to the specified individual from the piabetes monitor email.
#
# The username and password for the sender's email address should be added to a file named 'config.py'
#

# Method to email the status of the monitor
def sendEmail(message):
	# Import packages
	import smtplib, ssl
	# Import config variables
	import config

	## Email server information
	# Using Gmail with SSL encryption on port 465
	port = 465
	smtpServer = 'smtp.gmail.com'
	sender = config.sender
	pswd = config.pswd

	# Receiver information
	receiver = 'q.chris.d@gmail.com'

	## Create connection
	context = ssl.create_default_context()  # Creates context for ssl with default certs/authorization
	with smtplib.SMTP_SSL(smtpServer, port, context=context) as server:
		server.login(sender, pswd)
		server.sendmail(sender, receiver, message)

def formatEmail(subject, body):
	message = "Subject: {}\n\n{}".format(subject, body)
	return message



if __name__ == '__main__':
	sendEmail(formatEmail('test subject', 'test body'))
#	sendEmail('test')
