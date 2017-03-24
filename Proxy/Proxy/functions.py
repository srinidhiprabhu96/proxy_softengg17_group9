import hashlib
from django.utils.crypto import get_random_string
from auth_module.models import *

## Computing the hash of a password
def computeHash(raw_password):
	hasher = haslib.sha224(raw_password)
	return hasher.hexdigest()

# This function is being used instead of Django's inbuilt function because the mails weren't being sent when we used Django's inbuilt mail-sender. This needs to be looked into.
def sendEmail(name,email,code,account_label):
	print "Hi in sendEmail"
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
		print message
		p=MIMEText("Hello "+name+",\n\nThis is a verification mail from Group 9.\n"+message+"\nPlease click on the below link to verify your email ID.\n\nhttp://127.0.0.1:8000/verification/?code=" + code)
		content.attach(p)
		mail=smtplib.SMTP('smtp.gmail.com',587) #smtp server and its port number
		mail.ehlo()
		mail.starttls()
		mail.ehlo()
		mail.login(userEmail,userPassword)
		mail.sendmail(userEmail,content['TO'],content.as_string())
		mail.quit()
		return True
	except:
		return False
		
		
def generateCode():
	code = ''
	codeLength = 32		# For more security, so that guessing the code is difficult.
	flag = 1
	while flag != 0:		# Loop to ensure that the generated code doesn't exist already.
		code = get_random_string(length= codeLength, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		flag = len(SignUp.objects.filter(code=code))
	return code
