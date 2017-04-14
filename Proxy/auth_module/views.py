from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render,redirect
from django.contrib import messages
from django.template import Template, Context, RequestContext
import string
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from django.views.decorators.csrf import csrf_exempt
from auth_module.forms import *
from auth_module.models import *
from django.utils.crypto import get_random_string
from django.template import Context
from django.contrib.auth.models import User,Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
import random
import string
import re
import md5
import subprocess
from django.contrib.auth import logout
import logging


# View that displays the page for signup. Implemented by Srinidhi.
def signup(request):
	log = logging.getLogger('auth_module')
	log.info("Signing up")
	return render(request,'signup.html')

# When the logout button is clicked, this function is invoked(see urls.py). Implemented by Srinidhi
def logout_view(request):
	log = logging.getLogger('auth_module')
	log.info(request.user.first_name + " Logging out")
	logout(request)		# The current user is logged out.
	messages.info(request,"You have logged out successfully!")
	# Redirect to the login page.
	return redirect("/login/")

# This function is called when the user clicks on the signup button. Implemented by Srinidhi
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
					args = ["python","sendEmail.py",row.name,row.email,row.code,row.account]
					subprocess.Popen(args)	# Creates a new thread which handles the updating of attendance.
					messages.info(request,"Verification mail resent! Please check your inbox after some time.")
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
			args = ["python","sendEmail.py",name,email,code,account_label]
			subprocess.Popen(args)	# Creates a new thread which handles the updating of attendance.
			messages.info(request,"Verification mail sent! Please check your inbox after some time.")

			# Save the signup object only once mail is sent.
			signupobject.save()
			return render(request,'verify.html')
		else:
			messages.error(request,"Please enter an e-mail ID of the form \"abc@smail.iitm.ac.in\" or \"xyz@iitm.ac.in\"")
			return redirect("/signup/")

	# If it's not POST, just redirect to signup page.
	messages.error(request,"Please use the signup page to get a verification mail.")
	return redirect("/signup/")

# The method called when the user clicks on the verification link. Implemented by Srinidhi
def after_verify(request):
	if request.method == 'GET':		# Use get request to send the verification code.
		if not 'code' in request.GET.keys():
			return redirect("/signup/")
		verify_code = request.GET['code']
		try:
			# There must be atmost 1 row
			row = SignUp.objects.get(code=verify_code)		# We get either no rows or 1 row because code is ensured to be unique.
		except:
			row = None
		if not row:
			# The code does not exist.
			context = {}
			context['code_not_found'] = True

		else:
			# Verifying the mail and sending to password signup page.
			if row.status == '0':
				context = {}
				context['code_not_found'] = False
				context['name'] = row.name
				context['email'] = row.email
			else:
				# If already verified, mention so.
				context = {}
				context['verified'] = True
		return render(request,'password_signup_page.html',context)

	# Redirect to signup page if request method is not GET.
	return redirect("/signup/")

# Generates a 32 character code that is not present in the SignUp table. Implemented by Srinidhi
def generateCode():
	code = ''
	codeLength = 32		# For more security, so that guessing the code is difficult.
	flag = 1
	while flag != 0:		# Loop to ensure that the generated code doesn't exist already.
		code = get_random_string(length= codeLength, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		flag = len(SignUp.objects.filter(code=code))
	return code

# This method is called when the confirm signup button is clicked. Implemented by Srinidhi
@csrf_exempt
def finish_signup(request):
	if request.method == 'POST':
		# We use the django User class for maintaining the accounts.
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		confirm = request.POST['confirm_password']
		if password == confirm:
			hashed = make_password(password)		#Used for hashing the password. # Use a similar function authenticate while trying to login.
			try:
				row = SignUp.objects.get(email=email)	# Since email is unique
			except:
				row = None
			if row:	# E-mail field is unique in signup
				try:
					if row.account == '1':
						is_prof = True
					else:
						is_prof = False
					user = User(username=email,first_name=name,email=email,password=hashed,is_staff=is_prof)
					user.save()
					row.status = '1'
					row.save()
					return render(request,'finish_signup.html')
				except Exception as e:
					messages.error(request, "Some error occurred.")

			else:
				messages.error(request, "Could not find e-mail")	# There are no entries corresponding to this email.
		else:
			messages.error(request, "Passwords do not match")
		context = {}
		context['name'] = name
		context['email'] = email
		return render(request,'password_signup_page.html',context)
	return redirect("/signup/")

# Initially, the website goes to the login page. Implemented by Srinidhi.
def login_page(request):
	return render(request, 'login.html')

# Used for authenticating a user while logging in. Implemented by Pavan
@csrf_exempt
def auth(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():		# Get the entered data as a form.
			# Get form fields.
			e_mail = str(form.cleaned_data['email'])
			raw_password = str(form.cleaned_data['password'])
			try:
				user = authenticate(username=e_mail, password=raw_password)	# Check if the user exists
				if user:
					if user.is_active:
						log = logging.getLogger('auth_module')
						log.info(user.first_name + " Logging in")
						login(request,user)	# Make the user login, so that he can access subsequent pages before logging out.
						if user.is_staff:
							return redirect('/prof_home/')
						else:
							return redirect('/stud_home/')
					else:
						messages.error(request, "User isn't active. Please try again.")
				else:
					messages.error(request, "Password doesn't match or user does not exist. Please try again.")
			except:
				messages.error(request, "User doesn't exist. Please try again.")
		else:
			messages.error(request, "Please check your details and try again.")
	return redirect("/login/")
