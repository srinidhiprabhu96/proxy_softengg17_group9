from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
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

def signup(request):
	return render(request,'signup.html')
	
@csrf_exempt
def verify(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			name = str(form.cleaned_data['name'])
			email = str(form.cleaned_data['email'])
			code = generateCode()
			signupobject = SignUp(name=name,email=email,code=code)
			signupobject.save()
			sendEmail(name,email,code)
			return render(request,'verify.html')
		
		
	return render(request,'signup.html',{}) #If it fails, send the error context to signup. And display appropriately in signup.html page.


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
	mail.sendmail(userEmail,content['TO'],content.as_string())
	mail.quit()
