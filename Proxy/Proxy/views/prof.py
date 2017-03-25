from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render,redirect
from django.contrib import messages
from django.template import Template, Context, RequestContext
from django.views.decorators.csrf import csrf_exempt
from auth_module.forms import *
from auth_module.models import *
from django.utils.crypto import get_random_string
from django.template import Context
from django.contrib.auth.models import User,Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

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
