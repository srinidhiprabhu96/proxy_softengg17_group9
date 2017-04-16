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
from stud_module.forms import *
from django.template import RequestContext
import datetime
from glob import glob
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import logging

# This method is called when a student logs in. Implemented by Vinod and Hemanth.
@csrf_exempt
def stud_home(request):
	user = request.user
	if user.is_authenticated() and not user.is_staff:	# Display the page only if the user is logged in and is a student
	
		log = logging.getLogger('stud_module')
		log.info(request.user.first_name + " Student went to his home page")
		qs = Course.objects.filter(taken_by=user)	# get all courses taken by the student.
		percent = []	# For student's attendance percentage
		
		# For each course, find the attendance percentage.
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
		
	elif user.is_staff:		# If prof tries to access student page.
		messages.error(request,"You are not a student!")
		return redirect('/login/')
		
	else:	# If an un-authenticated user tries to access the page.
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# This method is called when a student wants to view a particular course. Implemented by Vinod and Hemanth.
@csrf_exempt
def stud_course(request, c_id):
	user = request.user
	if user.is_authenticated and not user.is_staff:
		log = logging.getLogger('stud_module')
		log.info(request.user.first_name + " Student went to " + c_id + " course page")
		
		try:									# Check if the student takes the course, and display the course page only if he takes the course.
			c = Course.objects.get(course_id=c_id,taken_by=user)
			return render(request, 'stud_course.html',{'course_id':c_id})
		except Exception as e:
			messages.error(request,"You are not registered for the course!")	# If the student doesn't take the course, redirect to login page with an error message.
			return redirect('/login/')
			
	elif user.is_staff:
		messages.error(request,"You are not a student!")
		return redirect('/login/')
		
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# This method is called when the student clicks the view daily report button. Implemented by Srinidhi
@csrf_exempt
def stud_daily_report(request):
	user = request.user
	if request.method == "POST":
		log = logging.getLogger('stud_module')
		log.info(request.user.first_name + " Student saw the daily report")
		
		if user.is_authenticated and not user.is_staff:
		
			form = DateForm(request.POST)	# Get the date.
			if form.is_valid():
				date = request.POST['date']
				str_date = date
				date = datetime.datetime.strptime(str_date,'%d/%m/%Y').date()
				attendances = Attendance.objects.filter(student=user,date=date)
				
				if len(attendances) == 0:
					return render(request, 'stud_daily_report.html',{'date':str_date})	# If there are no attendances, just send the date for rendering.
				else:
					return render(request, 'stud_daily_report.html', {'attendances':attendances, 'date':str_date})
			else:
				raise Http404("Enter a valid date")	# If date is not valid, raise a Http404. This is likely to happen when a POST request is made from an external source i.e. not by selecting the date in the datepicker.
				
		elif user.is_staff:
			messages.error(request,"You are not a student!")
			return redirect('/login/')
			
		else:
			messages.error(request,"You are not logged in.")
			return redirect('/login/')
	else:
		messages.error(request,"You are not allowed to view this page.")	# If a get request was made, display an error message.
		return redirect('/login/')

# This method is called when a student wants to view the queries he has raised. Implemented by Srinidhi.
def view_queries(request, c_id):
	user = request.user
	if user.is_authenticated and not user.is_staff:
		log = logging.getLogger('stud_module')
		log.info(request.user.first_name + " Student viewed " + c_id + " queries")
		
		try:										# Check if the student takes the course
			c = Course.objects.get(course_id=c_id,taken_by=user)
		except Exception as e:
			messages.error(request,"You are not registered for the course!")
			return redirect('/login/')
		
		queries = Query.objects.filter(course_id=c_id, student=user).order_by('-date')	# Gets the student's queries.
		if len(queries) == 0:
			return render(request, 'view_queries.html',{'course':c_id})
		else:
			return render(request, 'view_queries.html', {'queries':queries, 'course':c_id})
			
	elif user.is_staff:
		messages.error(request,"You are not a student!")
		return redirect('/login/')
		
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# This method is called when a student enters a query description and raises the query. Implemented by Srinidhi.
@csrf_exempt
def query(request, c_id):
	user = request.user
	if request.method == "POST":
		if request.user.is_authenticated and not request.user.is_staff:

			try:
				text = request.POST['query']
				date_str = request.POST['date']
			except:
				raise Http404("Enter valid data")
				
			date = datetime.datetime.strptime(date_str,"%d/%m/%Y")
			
			# Create a new query object and add it to the database.
			q = Query(course_id=c_id,student=request.user,date=date,query=text)
			q.save()
			messages.info(request,"Request successfully raised")
			log = logging.getLogger('stud_module')
			log.info(request.user.first_name + " Student submitted query for " + c_id)
			return render(request, 'stud_course.html',{'course_id':c_id})
			
		elif user.is_staff:
			messages.error(request,"You are not a student!")
			return redirect('/login/')
			
		else:
			messages.error(request,"You are not logged in.")
			return redirect('/login/')
			
	else:
		messages.error(request,"You are not allowed to view this page.")
		return redirect('/login/')

# This method is called when a student wants to raise a query. Implemented by Srinidhi.
def raise_query(request, c_id):
	user = request.user
	if request.method == "GET":	# Raise query pages are through GET requests.
	
		try:
			date = request.GET['date']
		except:
			raise Http404("Enter a valid date")
			
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

# This method is called when a student wants to view the history for a particular course on a particular date. Implemented by Srinidhi.
@csrf_exempt
def stud_history(request, c_id):
	user = request.user
	if request.method == "POST":
		if request.user.is_authenticated and not request.user.is_staff:
			# Control reaches here if the user is a student and is authenticated.
			try:
				date = request.POST['date']
			except:
				raise Http404("Enter a valid date")
				
			str_date = date
			date = datetime.datetime.strptime(str_date,'%d/%m/%Y').date()
			date_path = datetime.datetime.strftime(date,"%Y/%m/%d")
			
			try:
				prof_name = Course.objects.get(course_id=c_id).taught_by.username	# get the prof name for the course.
			except:
				messages.error(request,"You are not registered for the course!")
				return redirect('/login/')

			l =  glob(os.path.join(BASE_DIR, 'media/'+prof_name+'/'+c_id+'/'+date_path+'/*'))	# Get the images uploaded on that date.
			files = []
			for i in l:
				files.append(prof_name+"/"+c_id+"/"+date_path+"/"+os.path.basename(i))
			
			# Get the attendances for that date and course.
			att = Attendance.objects.filter(course_id=c_id,student=request.user,date=date)
			log = logging.getLogger('stud_module')
			log.info(request.user.first_name + " Student saw his history for " + c_id + " corresponding to the date " + str_date)
			
			if len(att) == 0:
				return render(request, 'stud_history.html',{'course':c_id, 'date':str_date})
			else:
				# If len(att) != 0, att must have 1 element.
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
