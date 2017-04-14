import sys
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

# This python script is called as a separate process when a person signs up. This file is written by Srinidhi.

# This function is being used instead of Django's inbuilt function because the mails weren't being sent when we used Django's inbuilt mail-sender. This needs to be looked into.
def sendEmail(name,email,code,account_label):
	# Setting the logger
	log = logging.getLogger('email_signup')
	hdlr = logging.FileHandler('logfile')
	hdlr.setLevel(logging.DEBUG)
	formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",datefmt="%d/%b/%Y %H:%M:%S")
	hdlr.setFormatter(formatter)
	log.addHandler(hdlr)
	log.setLevel(logging.DEBUG)
	
	# Sending the email
	try:
		userEmail='softwareengineeringroup9@gmail.com'
		userPassword = 'zecykaz2'
		content = MIMEMultipart()
		content['SUBJECT'] = 'Proxy E-mail verification'
		content['FROM'] = userEmail
		content['TO'] = email
		if account_label == '1':
			message = "You will be given professor rights in your account."
		else:
			message = "You will be given student rights in your account."
		p=MIMEText("Hello "+name+",\n\nThis is a verification mail from Group 9.\n"+message+"\nPlease click on the below link to verify your email ID.\n\nhttp://127.0.0.1:8000/verification/?code=" + code)
		content.attach(p)
		mail=smtplib.SMTP('smtp.gmail.com',587) #smtp server and its port number
		mail.ehlo()
		mail.starttls()
		mail.ehlo()
		mail.login(userEmail,userPassword)
		log.info("Generated mail content for signup")
		mail.sendmail(userEmail,content['TO'],content.as_string())
		mail.quit()
		log.info("Mail sent successfully to "+email)
		print "Mail sent"
	except Exception as e:
		log.debug(e)
		log.warning("Mail could not be sent")

	
if __name__ == "__main__":
	argv = sys.argv
	sendEmail(argv[1],argv[2],argv[3],argv[4])
