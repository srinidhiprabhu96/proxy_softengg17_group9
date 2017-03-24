from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render,redirect
from django.contrib import messages
from django.template import Template, Context, RequestContext
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from django.views.decorators.csrf import csrf_exempt
from auth_module.forms import *
from auth_module.models import *
from django.utils.crypto import get_random_string
from django.template import Context
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
import string
import re
import md5

def signup(request):
	return render(request,'signup.html')

@csrf_exempt
def before_verify(request):
	if request.method == 'POST':		# If the method is POST, it means the request is coming from the signup page.
		form = SignUpForm(request.POST)
		if form.is_valid():		# Get the entered data as a form.

			# Get form fields.
			name = str(form.cleaned_data['name'])
			email = str(form.cleaned_data['email'])
			try:
				match = SignUp.objects.get(email=email)
			except:
				match = None
			if match:		# If the email is already present, just resend the mail.
				row = match
				if row.status == '0':
					sendEmail(row.name,row.email,row.code,row.account)
					messages.info(request,"Verification mail resent!")
				else:
					messages.info(request,"This e-mail is already in use.")
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
			mailSent = sendEmail(name,email,code,account_label)

			if not mailSent:
				# If there is some error while sending the mail, display an error message.
				messages.error(request,"Something went wrong, please try again!")
				return redirect("/signup/")

			# Save the signup object only once mail is sent.
			signupobject.save()
			return render(request,'verify.html')
		
	# If it's not POST, just redirect to signup page.
	messages.error(request,"Please enter an e-mail ID of the form \"abc@smail.iitm.ac.in\" or \"xyz@iitm.ac.in\"")
	return redirect("/signup/")

# The method called when the user clicks on the verification link.
def after_verify(request):
	if request.method == 'GET':
		verify_code = request.GET['code']
		try:
			row = SignUp.objects.get(code=verify_code)		# We get either no rows or 1 row because code is ensured to be unique.
		except:
			row = None
		if not row:
			# The code does not exist.
			context = {}
			context['code_not_found'] = True

		else:
			# There must be only 1 element in row.
			if row.status == '0':
				context = {}
				context['code_not_found'] = False
				context['name'] = row.name
				context['email'] = row.email
			else:
				context = {}
				context['verified'] = True
		return render(request,'password_signup_page.html',Context(context))

	# Redirect to signup page if request method is not GET.
	return redirect("/signup/")

@csrf_exempt
def finish_signup(request):
	if request.method == 'POST':
		# We use the django User class for maintaining the accounts.
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		confirm = request.POST['confirm_password']
		if password == confirm:

			# Add hashed password here.
			hashed = make_password(password)		#Used for hashing the password. # Use a similar function check_password while trying to login.
			try:
				row = SignUp.objects.get(email=email)	# Since email is unique
			except:
				row = None
			if row:	# E-mail field is unique in signup
				try:
					user = ProxyUser(username=email,first_name=name,email=email,password=hashed,account_type=row.account)
					user.save()
					row.status = '1'
					row.save()
				except:
					pass
				return render(request,'finish_signup.html')
			else:
				messages.error(request, "Could not find e-mail")	# There are no entries corresponding to this email.
		else:
			messages.error(request, "Passwords do not match")
		context = {}
		context['name'] = name
		context['email'] = email
		return render(request,'password_signup_page.html',Context(context))
	return redirect("/signup/")

def generateCode():
	code = ''
	codeLength = 32		# For more security, so that guessing the code is difficult.
	flag = 1
	while flag != 0:		# Loop to ensure that the generated code doesn't exist already.
		code = get_random_string(length= codeLength, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		flag = len(SignUp.objects.filter(code=code))
	return code

# This function is being used instead of Django's inbuilt function because the mails weren't being sent when we used Django's inbuilt mail-sender. This needs to be looked into.
def sendEmail(name,email,code,account_label):
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
		mail.sendmail(userEmail,content['TO'],content.as_string())
		mail.quit()
		return True
	except:
		return False

def login(request):
	return render(request, 'login.html')

@csrf_exempt
def auth(request):
	if request.method == 'POST':
		# print request.POST
		form = LoginForm(request.POST)
		# print form
		if form.is_valid():		# Get the entered data as a form.
			# Get form fields.
			e_mail = str(form.cleaned_data['email'])
			raw_password = str(form.cleaned_data['password'])
			try:
				user_obj = ProxyUser.objects.get(email = e_mail)
				is_password = user_obj.check_password(raw_password)
				# print is_password
				if is_password:
					if user_obj.ACCOUNT_TYPE == 0:
						return redirect('/student_home/')
					else:
						return redirect('/prof_home/')
				else:
					messages.error(request, "Password doesn't match. Please try again.")
			except:
				messages.error(request, "User doesn't exist. Please try again.")
		else:
			messages.error(request, "Please check your details and try again.")
	return redirect("/login/")


@csrf_exempt
def prof_home(request):
	# add context as third arg to render
	if request.user.is_authenticated():
		return render(request, 'prof_home.html')
	else:
		return redirect('/signup/')

def prof_course(request):
	# add context as third arg to render
	return render(request, 'prof_course.html')

def add_stud(request):
	# add context as third arg to render
	return render(request, 'add_stud.html')

def daily_report(request):
	# add context as third arg to render
	return render(request, 'daily_report.html')

def prof_history(request):
	# add context as third arg to render
	return render(request, 'prof_history.html')

def take_attendance(request):
	# add context as third arg to render
	return render(request, 'take_attendance.html')

def prof_queries(request):
	# add context as third arg to render
	return render(request, 'prof_queries.html')
