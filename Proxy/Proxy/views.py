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

def signup(request):
	return render(request,'signup.html')
	
def verify(request):
	sendEmail()
	return render(request,'verify.html')
	
def sendEmail():
	userEmail='softwareengineeringroup9@gmail.com'
	userPassword = 'zecykaz2'
	content = MIMEMultipart()
	content['SUBJECT'] = 'Proxy- E-mail verification'
	content['FROM'] = userEmail
	content['TO'] = 'cs14b028@smail.iitm.ac.in'
	p=MIMEText("Hello ,\n\nThis is a verification mail from Group 9.")
	content.attach(p)
	mail=smtplib.SMTP('smtp.gmail.com',587) #smtp server and its port number
	mail.ehlo()
	mail.starttls()
	mail.ehlo()
	mail.login(userEmail,userPassword)
	mail.sendmail(userEmail,content['TO'],content.as_string())
	mail.quit()
