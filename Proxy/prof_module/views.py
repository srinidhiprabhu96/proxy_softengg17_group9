# -*- coding: utf-8 -*-
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
from prof_module.models import *
from prof_module.forms import *
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import datetime
import subprocess
from api_wrappers import *
from glob import glob

import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Implemented by Pavan
# Called when prof views the homepage
@csrf_exempt
def prof_home(request):
	# Similar structure is followed throughout all the views. Similar won't be commented
	if request.user.is_authenticated() and request.user.is_staff:	# display only if the user is logged in and a prof
		log = logging.getLogger('prof_module')
		log.info(request.user.first_name + " Professor went to his home page")
		qs = Course.objects.filter(taught_by=request.user)
		return render(request, 'prof_home.html', {'courses':qs})
	elif not request.user.is_staff:									# display if the user is logged in but not a prof
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:															# display if the user is not logged in
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# Implemented by Pavan
# Called when prof views the course page
@csrf_exempt
def prof_course(request, c_id):
	if request.user.is_authenticated() and request.user.is_staff:
		log = logging.getLogger('prof_module')
		log.info(request.user.first_name + " Professor went to " + c_id + " course page")
		try:
			c = Course.objects.get(course_id=c_id,taught_by=request.user)	# get the course corresponding to c_id
			return render(request, 'prof_course.html',{'course_id':c_id})
		except Exception as e:
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():												# raise error if the prof doesn't teach c_id
				raise Http404("You don't teach the course!")
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# Implemented by Pavan
# Called when prof views the day-wise report
@csrf_exempt
def daily_report(request, c_id, y, m, d):
	if request.user.is_authenticated() and request.user.is_staff:
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():		# to ensure that the prof teaches the course 'c_id'. This is present in all course-wise views
			raise Http404("You don't teach the course!")
		date_str = y+'/'+m+'/'+d
		log = logging.getLogger('prof_module')
		log.info(request.user.first_name + " Professor saw the daily report of " + c_id + " corresponding to the date " + date_str)
		l =  glob(os.path.join(BASE_DIR, 'media/'+request.user.username+'/'+c_id+'/'+date_str+'/*'))	# get all the images for the course 'c_id' on the date 'date_str'
		files = []
		for i in l:
			files.append(os.path.basename(i))		# get the corresponding file names
		try:
			date_obj = datetime.date(int(y),int(m),int(d))	# create date obj
		except Exception as e:
			raise Http404("Invalid date!")
		try:
			query_set = Attendance.objects.filter(course_id=c_id,prof=request.user,date=date_obj)	# get attendance data
			return render(request, 'daily_report.html',{'course_id':c_id, 'date':date_obj, 'date_url':date_str, 'files':files, 'attendance':query_set})
		except Exception as e:
			raise e
			raise Http404("You don't teach the course!")
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# Implemented by Pavan
# Called when prof submits the date in view history.
@csrf_exempt
def prof_history(request, c_id):
	if request.user.is_authenticated() and request.user.is_staff:
		log = logging.getLogger('prof_module')
		log.info(request.user.first_name + " Professor saw the history of a " + c_id + " course")
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				raise Http404("You don't teach the course!")
		try:
			if request.method == 'POST':				# submitting date is a post request
				date_str = request.POST.get('date')		# get the date
				date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')		# parse it
				date_str = date_obj.strftime('%Y/%m/%d')	# format it as reqd
				return redirect('/daily_report/'+c_id+'/'+date_str+'/')
			else:
				raise Http404("You Haven't entered any date!")
		except Exception as e:
			# raise e
			raise Http404("You entered the wrong date format!")
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# Implemented by Pavan
# Called when prof views take attendance
# This is just a view request. The uploaded pics will be 'post'ed to take_attendance()
def upload_class_photos(request, c_id):
	if request.user.is_authenticated() and request.user.is_staff:
		log = logging.getLogger('prof_module')
		log.info(request.user.first_name + " Professor uploaded class photos for " + c_id)
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			raise Http404("You don't teach the course!")
		return render(request, 'upload_class_photos.html', {'course_id':c_id})
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# Implemented by Pavan
# The uploaded images are 'post'ed here
@csrf_exempt
def take_attendance(request, c_id):
	if request.user.is_authenticated() and request.user.is_staff and request.method == 'POST':
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			raise Http404("You don't teach the course!")
		form = ClassImagesForm(request.POST, request.FILES)
		if form.is_valid:
			try:
				# get date string. parse and format as reqd
				date_str = request.POST.get('date')
				date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
				date_str = date_obj.strftime('%Y-%m-%d')
				date_str2 = date_obj.strftime('%Y/%m/%d')
			except Exception as e:
				raise Http404("You entered the wrong date format!")
			images = request.FILES.getlist('myfiles')	# get the images
			paths = []
			for i in images:
				# save them
				path = default_storage.save(request.user.username+'/'+c_id+'/'+date_str2+'/'+i.name, ContentFile(i.read()))
				paths += [os.path.join(settings.MEDIA_ROOT, path)]

			## Added by Srinidhi - starting a new process for making API calls to improve user experience.
			date = date_str	# Currently setting today's date, change the date here.  -- Changed
			args = []
			args.append("python")
			args.append("searchFace.py")
			args.append(c_id)
			args.append(date)
			args = args + paths
			subprocess.Popen(args)	# Creates a new thread which handles the updating of attendance.
			## End of added by Srinidhi

			log = logging.getLogger('prof_module')
			log.info(request.user.first_name + " Professor uploaded files for " + c_id + " and took attendance for date " + date)

			messages.success(request, 'Files uploaded successfully!')
		else:
			messages.error(request, 'Unable to upload files. Try again.')
		return redirect('/upload_class_photos/'+c_id+'/')
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	elif request.method != 'POST':
		messages.error(request,"You haven't uploaded any images!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# Implemented by Pavan
@csrf_exempt
def prof_queries(request, c_id):
	if request.user.is_authenticated() and request.user.is_staff:
		log = logging.getLogger('prof_module')
		log.info(request.user.first_name + " Professor saw queries for " + c_id)
		try:
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				raise Http404("You dont teach the course!")
			if request.method == 'POST':
				# if the prof wants to change the attendance status
				res = request.POST.get('query').split()
				# res[0] is the 'id' and res[1] is the new attendance status.
				temp_query = Query.objects.get(id= res[0])	# get the query object
				temp_query.status = '1'		# change the query status
				temp_query.save()			# save it
				try:
					# get the attendance object
					temp_att = Attendance.objects.get(course_id=c_id,student=temp_query.student,date=temp_query.date)
				except Exception as e:
					raise e
				temp_att.is_present = res[1]	# change the attendance status
				temp_att.save()					# save it

			# order the queries in descending order of date.
			query_set = Query.objects.filter(course_id=c_id).order_by('-date')
			att_set = []
			for q in query_set:
				try:
					# corresponding attendance statuses. They are used in the html.
					att = Attendance.objects.get(course_id=c_id,student=q.student,date=q.date)
					att_set.append(att.is_present)
				except Exception as e:
					raise e

			return render(request, 'prof_queries.html',{'course_id':c_id, 'list':zip(query_set,att_set)})
		except Exception as e:
			# raise e
			raise Http404("You don't teach the course!")
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# Implemented by Pavan
# Called when the prof hits 'view_images' in the 'view_queries' page.
# Supposed to display images corresponding to the query.
@csrf_exempt
def view_images(request):
	if request.user.is_authenticated() and request.user.is_staff:
		cr = Course.objects.filter(course_id=request.POST.get('course'), taught_by=request.user)
		if not cr.exists():
			raise Http404("You don't teach the course!")
		if request.method == 'POST':	# data is 'post'ed
			# get date, course
			date_str = request.POST.get('date')
			course = request.POST.get('course')
			# parse and format the date as reqd
			date_obj = datetime.datetime.strptime(date_str, '%B %d, %Y')
			date_str = date_obj.strftime('%Y/%m/%d')
			# get the file names
			images = [os.path.basename(x) for x in glob(os.path.join(BASE_DIR, 'media/'+request.user.username+'/'+course+'/'+date_str+'/*'))]
			for i in range(len(images)):
				# send the file path via the context
				images[i] = request.user.username+'/'+course+'/'+date_str+'/' + images[i]
			return render(request, 'view_images.html', {'list':images,'course':course})
		else:
			raise Http404('You haven\'t selected the query!')
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')
