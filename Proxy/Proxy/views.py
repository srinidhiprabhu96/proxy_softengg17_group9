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
import random
import string
import re

def signup(request):
	return render(request,'signup.html')
	
@csrf_exempt
def verify(request):
	if request.method == 'POST':		# If the method is POST, it means the request is coming 
		form = SignUpForm(request.POST)
		if form.is_valid():
			name = str(form.cleaned_data['name'])
			email = str(form.cleaned_data['email'])
			prof_mail_re = re.compile(".+@iitm.ac.in")
			student_mail_re = re.compile(".+@smail.iitm.ac.in")
			prof_match = prof_mail_re.match(email)
			if prof_match:
				account_label = '1'
			else:
				student_match = student_mail_re.match(email)
				if student_match:
					account_label = '0'
				else:
					messages.error(request,"Please enter an e-mail ID of the form \"abc@smail.iitm.ac.in\" or \"xyz@iitm.ac.in\"")
					return redirect("/signup/")
					
			code = generateCode()
			signupobject = SignUp(name=name,email=email,code=code,account=account_label)
			signupobject.save()
			sendEmail(name,email,code)
			return render(request,'verify.html')
		
		
	return redirect("/signup/")


def generateCode():
	code = ''
	codeLength = 6
	for i in range(0,codeLength):
		code += random.choice(string.letters)
	return code
	
def sendEmail(name,email,code):
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
	try:
		mail.sendmail(userEmail,content['TO'],content.as_string())
	except:
		pass
	# According to success or failure, handle appropriately
	mail.quit()
