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
from django.template import RequestContext
import datetime
from glob import glob
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def stud_home(request):
	user = request.user
	if user.is_authenticated() and not user.is_staff:	# Display the page only if the user is logged in and is a student
		qs = Course.objects.filter(taken_by=user)
		percent = []	# For student's attendance percentage
		for a in qs:
			totalno = Attendance.objects.filter(student=user,course_id=a.course_id).count()
			presentno = Attendance.objects.filter(student=user,course_id=a.course_id,is_present=1).count()
			try:
				currpercent = (100*presentno)/totalno
				percent.append(currpercent)
			except:
				percent.append(0)
				pass
		return render(request, 'stud_home.html', {'course_percent':zip(qs,percent)})
	elif user.is_staff:
		messages.error(request,"You are not a student!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

@csrf_exempt
def stud_course(request, c_id):
	user = request.user
	if user.is_authenticated and not user.is_staff:
		try:										# Check if the student takes the course
			c = Course.objects.get(course_id=c_id,taken_by=user)	
			return render(request, 'stud_course.html',{'course_id':c_id})
		except Exception as e:
			messages.error(request,"You are not registered for the course!")
			return redirect('/login/')
	elif user.is_staff:
		messages.error(request,"You are not a student!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

@csrf_exempt
def stud_daily_report(request):
	user = request.user
	if request.method == "POST":
		if user.is_authenticated and not user.is_staff:
			date = request.POST['date']
			str_date = date
			#print date
			date = datetime.datetime.strptime(str_date,'%d/%m/%Y').date()
			#print date
			attendances = Attendance.objects.filter(student=user,date=date)
			if len(attendances) == 0:
				#messages.error(request,"No history to display")
				return render(request, 'stud_daily_report.html',{'date':str_date})
			else:
				return render(request, 'stud_daily_report.html', {'attendances':attendances, 'date':str_date})
		elif user.is_staff:
			messages.error(request,"You are not a student!")
			return redirect('/login/')
		else:
			messages.error(request,"You are not logged in.")
			return redirect('/login/')
	else:
		messages.error(request,"You are not allowed to view this page.")
		return redirect('/login/')

# Better if we can put date here also
def view_queries(request, c_id):
	user = request.user
	if user.is_authenticated and not user.is_staff:
		queries = Query.objects.filter(course_id=c_id, student=user).order_by('-date')	# Gets the student's queries.
		if len(queries) == 0:
			#messages.error(request,"No queries to display")
			return render(request, 'view_queries.html',{'course':c_id})
		else:
			return render(request, 'view_queries.html', {'queries':queries, 'course':c_id})
	elif user.is_staff:
		messages.error(request,"You are not a student!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

@csrf_exempt	
def query(request, c_id):
	user = request.user
	if request.method == "POST":
		if request.user.is_authenticated and not request.user.is_staff:
			# Use a form for handling boundary cases.
			print request.POST
			text = request.POST['query']
			date_str = request.POST['date']
			print date_str
			date = datetime.datetime.strptime(date_str,"%d/%m/%Y")
			print date
			q = Query(course_id=c_id,student=request.user,date=date,query=text)
			q.save()
			messages.info(request,"Request successfully raised")
			return render(request, 'stud_course.html',{'course_id':c_id})
		else:
			pass # Handle error here
	return render(request, 'stud_course.html',{'course_id':c_id})

# Add a date field in raise query also
def raise_query(request, c_id):
	user = request.user
	if request.method == "GET":
		date = request.GET['date']
		if request.user.is_authenticated and not request.user.is_staff:
			try:										# Check if the student takes the course
				c = Course.objects.get(course_id=c_id,taken_by=user)	
				return render(request, 'raise_query.html',{'course':c_id,'date':date})
			except Exception as e:
				messages.error(request,"You are not registered for the course!")
				return redirect('/login/')
		elif user.is_staff:
			messages.error(request,"You are not a student!")
			return redirect('/login/')
		else:
			messages.error(request,"You are not logged in.")
			return redirect('/login/')
	else:
		messages.error(request,"You are not allowed to view this page.")
		return redirect('/login/')
	
# Add a date field in stud history also
@csrf_exempt
def stud_history(request, c_id):
	user = request.user
	if request.method == "POST":
		if request.user.is_authenticated and not request.user.is_staff:
			# Control reaches here if the user is a student and is authenticated.
			date = request.POST['date']
			str_date = date
			date = datetime.datetime.strptime(str_date,'%d/%m/%Y').date()
			date_path = datetime.datetime.strftime(date,"%Y/%m/%d")
			try:
				prof_name = Course.objects.get(course_id=c_id).taught_by.username
			except:
				messages.error(request,"You are not registered for the course!")
				return redirect('/login/')
				
			l =  glob(os.path.join(BASE_DIR, 'media/'+prof_name+'/'+c_id+'/'+date_path+'/*'))
			files = []
			for i in l:
				files.append(prof_name+"/"+c_id+"/"+date_path+"/"+os.path.basename(i))
			
			att = Attendance.objects.filter(course_id=c_id,student=request.user,date=date)
			if len(att) == 0:
				#messages.error(request,"No history to display")
				return render(request, 'stud_history.html',{'course':c_id, 'date':str_date})
			else:
				is_present = att[0].is_present
				return render(request, 'stud_history.html', {'attendance':is_present, 'course':c_id, 'files':files, 'date':str_date})
		elif user.is_staff:
			messages.error(request,"You are not a student!")
			return redirect('/login/')
		else:
			messages.error(request,"You are not logged in.")
			return redirect('/login/')
	else:
		messages.error(request,"You are not allowed to view this page.")
		return redirect('/login/')
