from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render,redirect
from django.contrib import messages
from django.template import Template, Context, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.template import Context
from django.contrib.auth.models import User,Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from auth_module.models import *
from auth_module.forms import *
from stud_module.models import *
from prof_module.models import *

@csrf_exempt
def stud_home(request):
	# add context as third arg to render
	if request.user.is_authenticated():
		# print request.user.username
		qs = Course.objects.filter(taught_by=request.user)
		return render(request, 'stud_home.html', {'courses':qs})
	else:
		return redirect('/login/')

@csrf_exempt
def stud_course(request):
	# add context as third arg to render
	if request.user.is_authenticated:
		try:
			return render(request, 'stud_course.html')
		except Exception as e:
			raise Http404("You don't take the course!")
	else:
		return redirect('/login/')

# def store_stud: doubt - where to create new student

def stud_daily_report(request):
	# add context as third arg to render
	return render(request, 'stud_daily_report.html')

def stud_queries(request):
	# add context as third arg to render
	return render(request, 'stud_queries.html')

def raise_query(request):
	# add context as third arg to render
	return render(request, 'raise_query.html')

def stud_queries(request):
	# add context as third arg to render
	return render(request, 'stud_queries.html')

def stud_history(request):
	# add context as third arg to render
	return render(request, 'stud_history.html')
