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

@csrf_exempt
def prof_home(request):
	# add context as third arg to render
	log = logging.getLogger('prof_module')
	log.debug(request.user.first_name + " Professor went to his home page")
	if request.user.is_authenticated() and request.user.is_staff:
		# print request.user.username
		qs = Course.objects.filter(taught_by=request.user)
		return render(request, 'prof_home.html', {'courses':qs})
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')


@csrf_exempt
def prof_course(request, c_id):
	# add context as third arg to render
	log = logging.getLogger('prof_module')
	log.debug(request.user.first_name + " Professor went to " + c_id + " course page")
	if request.user.is_authenticated() and request.user.is_staff:
		try:
			c = Course.objects.get(course_id=c_id,taught_by=request.user)
			return render(request, 'prof_course.html',{'course_id':c_id})
		except Exception as e:
			#raise Http404("You don't teach the course!")
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				raise Http404("You don't teach the course!")
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

# @csrf_exempt
# def add_stud(request, c_id):
# 	# add context as third arg to render
# 	if request.user.is_authenticated:
# 		return render(request, 'add_stud.html')
# 	else:
# 		return redirect('/login/')

# def store_stud: doubt - where to create new student

@csrf_exempt
def daily_report(request, c_id, y, m, d):
	# add context as third arg to render
	if request.user.is_authenticated() and request.user.is_staff:
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			raise Http404("You don't teach the course!")
		# if request.method == 'POST':
		# 	obj = Attendance.objects.get(id = request.POST.get('id'))
		# 	if obj.is_present == '0':
		# 		obj.is_present = '1'
		# 	else:
		# 		obj.is_present = '0'
		# 	obj.save()
		date_str = y+'/'+m+'/'+d
		log = logging.getLogger('prof_module')
		log.debug(request.user.first_name + " Professor saw the daily report of " + c_id + " corresponding to the date " + date_str)
		# print os.path.join(BASE_DIR, 'media/'+request.user.username+'/'+c_id+'/'+date_str+'/*')
		l =  glob(os.path.join(BASE_DIR, 'media/'+request.user.username+'/'+c_id+'/'+date_str+'/*'))
		files = []
		for i in l:
			files.append(os.path.basename(i))
		try:
			date_obj = datetime.date(int(y),int(m),int(d))
		except Exception as e:
			raise Http404("Invalid date!")
		try:
			query_set = Attendance.objects.filter(course_id=c_id,prof=request.user,date=date_obj)
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

@csrf_exempt
def prof_history(request, c_id):
	log = logging.getLogger('prof_module')
	log.debug(request.user.first_name + " Professor saw the history of a " + c_id + " course")
	# add context as third arg to render
	if request.user.is_authenticated() and request.user.is_staff:
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			#raise Http404("You dont teach the course!")
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				raise Http404("You don't teach the course!")
		try:
			# query_set = Attendance.objects.filter(course_id=c_id,prof=request.user)
			# dates = []
			# for i in query_set:
			# 	tmp_date = i.date.strftime('%Y/%m/%d')
			# 	if tmp_date not in dates:
			# 		dates.append(tmp_date)
			# dates.sort(reverse=True)
			if request.method == 'POST':
				date_str = request.POST.get('date')
				date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
				date_str = date_obj.strftime('%Y/%m/%d')
				return redirect('/daily_report/'+c_id+'/'+date_str+'/')
			else:
				raise Http404("You Haven't entered any date!")
			# return render(request, 'prof_history.html',{'course_id':c_id})
		except Exception as e:
			# raise e
			raise Http404("You entered the wrong date format!")
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

def upload_class_photos(request, c_id):
	log = logging.getLogger('prof_module')
	log.debug(request.user.first_name + " Professor uploaded class photos for " + c_id)
	if request.user.is_authenticated() and request.user.is_staff:
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

@csrf_exempt
def take_attendance(request, c_id):
	# add context as third arg to render
	"""cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
	if not cr.exists():
		raise Http404("You don't teach the course!")
		return redirect('/login/')"""
	if request.user.is_authenticated() and request.user.is_staff and request.method == 'POST':
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			raise Http404("You don't teach the course!")
		form = ClassImagesForm(request.POST, request.FILES)
		if form.is_valid:
			try:
				date_str = request.POST.get('date')
				date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
				date_str = date_obj.strftime('%Y-%m-%d')
				date_str2 = date_obj.strftime('%Y/%m/%d')
			except Exception as e:
				raise Http404("You entered the wrong date format!")
			images = request.FILES.getlist('myfiles')
			paths = []
			for i in images:
				# print i.name
				path = default_storage.save(request.user.username+'/'+c_id+'/'+date_str2+'/'+i.name, ContentFile(i.read()))
				paths += [os.path.join(settings.MEDIA_ROOT, path)]

			## Added by SP - search in faceset
			date = date_str	# Currently setting today's date, change the date here.  -- Changed
			args = []
			args.append("python")
			args.append("searchFace.py")
			args.append(c_id)
			args.append(date)
			args = args + paths
			#print args
			subprocess.Popen(args)	# Creates a new thread which handles the updating of attendance.
			## End of added by SP

			log = logging.getLogger('prof_module')
			log.debug(request.user.first_name + " Professor uploaded files for " + c_id + " and took attendance for date " + date)

			messages.success(request, 'Files uploaded successfully!')
		else:
			messages.error(request, 'Unable to upload files. Try again.')
		return redirect('/upload_class_photos/'+c_id+'/')
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	elif request.method != 'POST':
		#raise Http404("You haven't uploaded any images!")
		messages.error(request,"You haven't uploaded any images!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

@csrf_exempt
def prof_queries(request, c_id):
	# add context as third arg to render
	log = logging.getLogger('prof_module')
	log.debug(request.user.first_name + " Professor saw queries for " + c_id)
	if request.user.is_authenticated() and request.user.is_staff:
		try:
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				raise Http404("You dont teach the course!")
			if request.method == 'POST':
				res = request.POST.get('query').split()
				temp_query = Query.objects.get(id= res[0])
				temp_query.status = '1'
				temp_query.save()
				try:
					temp_att = Attendance.objects.get(course_id=c_id,student=temp_query.student,date=temp_query.date)
				except Exception as e:
					raise e
				temp_att.is_present = res[1]
				temp_att.save()


			query_set = Query.objects.filter(course_id=c_id).order_by('-date')
			# print query_set
			att_set = []
			for q in query_set:
				try:
					att = Attendance.objects.get(course_id=c_id,student=q.student,date=q.date)
					att_set.append(att.is_present)
				except Exception as e:
					pass

				#print att
			return render(request, 'prof_queries.html',{'course_id':c_id, 'list':zip(query_set,att_set)})
		except Exception as e:
			raise e
			#raise Http404("You don't teach the course!")
			raise Http404("You don't teach the course!")
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

@csrf_exempt
def view_images(request):
	if request.user.is_authenticated() and request.user.is_staff:
		cr = Course.objects.filter(course_id=request.POST.get('course'), taught_by=request.user)
		if not cr.exists():
			raise Http404("You don't teach the course!")
		if request.method == 'POST':
			date_str = request.POST.get('date')
			# user = request.POST.get('username')
			course = request.POST.get('course')
			date_obj = datetime.datetime.strptime(date_str, '%B %d, %Y')
			date_str = date_obj.strftime('%Y/%m/%d')
			images = [os.path.basename(x) for x in glob(os.path.join(BASE_DIR, 'media/'+request.user.username+'/'+course+'/'+date_str+'/*'))]
			for i in range(len(images)):
				images[i] = request.user.username+'/'+course+'/'+date_str+'/' + images[i]
			# print images
			return render(request, 'view_images.html', {'list':images,'course':course})
		else:
			raise Http404('You haven\'t selected the query!')
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')
