from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render,redirect
from django.contrib import messages
import string
import smtplib
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from django.views.decorators.csrf import csrf_exempt
from auth_module.forms import *
from auth_module.models import *
from django.utils.crypto import get_random_string
import random
import string
import re

def signup(request):
	return render(request,'signup.html')
	
@csrf_exempt
def verify(request):
	if request.method == 'POST':		# If the method is POST, it means the request is coming from the signup page.
		form = SignUpForm(request.POST)
		if form.is_valid():		# Get the entered data as a form.
		
			# Get form fields.
			name = str(form.cleaned_data['name'])
			email = str(form.cleaned_data['email'])
			match = SignUp.objects.filter(email=email)
			if len(match) > 0:		# If the email is already present, just resend the mail.
				row = match[0]
				sendEmail(row.name,row.email,row.code)
				messages.info(request,"Verification mail resent!")
				return render(request,'verify.html')
				
			# If no match for the email found in the table.
			prof_mail_re = re.compile(".+@iitm.ac.in")
			student_mail_re = re.compile(".+@smail.iitm.ac.in")
			
			# Try matching with the prof and student mail reg-ex
			prof_match = prof_mail_re.match(email)
			if prof_match:
				account_label = '1'
			else:
				student_match = student_mail_re.match(email)
				if student_match:
					account_label = '0'
				else:
					
					# If both reg-exs don't match display an error message.
					messages.error(request,"Please enter an e-mail ID of the form \"abc@smail.iitm.ac.in\" or \"xyz@iitm.ac.in\"")
					return redirect("/signup/")		# Redirects to signup URL.
			
			# Control reaches here if it's either a student or prof account.		
			code = generateCode()
			signupobject = SignUp(name=name,email=email,code=code,account=account_label)
			mailSent = sendEmail(name,email,code)
			
			if not mailSent:
				# If there is some error while sending the mail, display an error message.
				messages.error(request,"Something went wrong, please try again!")
				return redirect("/signup/")
			
			# Save the signup object only once mail is sent.
			signupobject.save()
			return render(request,'verify.html')
		
	# If it's not POST, just redirect to signup page.	
	return redirect("/signup/")


def generateCode():
	code = ''
	codeLength = 6
	flag = 1
	while flag != 0:		# Loop to ensure that the generated code doesn't exist already.
		code = get_random_string(length= codeLength, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		flag = len(SignUp.objects.filter(code=code))
	return code
	
# This function is being used instead of Django's inbuilt function because the mails weren't being sent when we used Django's inbuilt mail-sender. This needs to be looked into.
def sendEmail(name,email,code):
	try:
		userEmail='softwareengineeringroup9@gmail.com'
		userPassword = 'zecykaz2'
		content = MIMEMultipart()
		content['SUBJECT'] = 'Proxy E-mail verification'
		content['FROM'] = userEmail
		content['TO'] = email
		p=MIMEText("Hello "+name+",\n\nThis is a verification mail from Group 9. Please click on the below link to verify your email ID.\n\nhttp://127.0.0.1:8080/verification/?code=" + code)
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
