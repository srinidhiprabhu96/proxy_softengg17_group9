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

@csrf_exempt
def prof_home(request):
	# add context as third arg to render
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
	if request.user.is_authenticated() and request.user.is_staff:
		try:
			c = Course.objects.get(course_id=c_id,taught_by=request.user)
			return render(request, 'prof_course.html',{'course_id':c_id})
		except Exception as e:
			#raise Http404("You don't teach the course!")
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				messages.error(request,"You don't teach the course!")
				return redirect('/login/')
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

def daily_report(request, c_id, y, m, d):
	# add context as third arg to render
	if request.user.is_authenticated() and request.user.is_staff:
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				messages.error(request,"You don't teach the course!")
				return redirect('/login/')
		try:
			date_str = d+'/'+m+'/'+y
			date_obj = datetime.date(int(y),int(m),int(d))
		except Exception as e:
			raise Http404("Invalid date!")
		try:
			query_set = Attendance.objects.filter(course_id=c_id,prof=request.user,date=date_obj)
			return render(request, 'daily_report.html',{'course_id':c_id, 'date':date_str, 'attendance':query_set})
		except Exception as e:
			# raise e
			#raise Http404("You don't teach the course!")
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				messages.error(request,"You don't teach the course!")
				return redirect('/login/')
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

def prof_history(request, c_id):
	# add context as third arg to render
	if request.user.is_authenticated() and request.user.is_staff:
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			#raise Http404("You dont teach the course!")
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				messages.error(request,"You don't teach the course!")
				return redirect('/login/')
		try:
			query_set = Attendance.objects.filter(course_id=c_id,prof=request.user)
			dates = []
			for i in query_set:
				tmp_date = i.date.strftime('%Y/%m/%d')
				if tmp_date not in dates:
					dates.append(tmp_date)
			dates.sort(reverse=True)
			return render(request, 'prof_history.html',{'course_id':c_id, 'dates':dates})
		except Exception as e:
			# raise e
			#raise Http404("You don't teach the course!")
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				messages.error(request,"You don't teach the course!")
				return redirect('/login/')
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')

def upload_class_photos(request, c_id):
	if request.user.is_authenticated() and request.user.is_staff:
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			messages.error(request,"You don't teach the course!")
			return redirect('/login/')
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
		messages.error(request,"You don't teach the course!")
		return redirect('/login/')"""
	if request.user.is_authenticated() and request.user.is_staff and request.method == 'POST':
		cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
		if not cr.exists():
			messages.error(request,"You don't teach the course!")
			return redirect('/login/')
		form = ClassImagesForm(request.POST, request.FILES)
		if form.is_valid:
			images = request.FILES.getlist('myfiles')
			paths = []
			for i in images:
				# print i.name
				path = default_storage.save(request.user.username+'/'+c_id+'/'+datetime.date.today().strftime('%Y/%m/%d')+'/'+i.name, ContentFile(i.read()))
				paths += [os.path.join(settings.MEDIA_ROOT, path)]
				
			## Added by SP - search in faceset
			args = []
			args.append("python")
			args.append("searchFace.py")
			args.append(c_id)
			args = args + paths
			#print args
			subprocess.Popen(args)	# Creates a new thread which handles the updating of attendance.
			## End of added by SP
				
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

def prof_queries(request, c_id):
	# add context as third arg to render
	if request.user.is_authenticated() and request.user.is_staff:
		try:
			cr = Course.objects.filter(course_id=c_id, taught_by=request.user)
			if not cr.exists():
				raise Http404("You dont teach the course!")
			query_set = Query.objects.filter(course_id=c_id).order_by('-date')

			return render(request, 'prof_queries.html',{'course_id':c_id, 'queries':query_set})
		except Exception as e:
			# raise e
			#raise Http404("You don't teach the course!")
			messages.error(request,"You don't teach the course!")
			return redirect('/login/')
	elif not request.user.is_staff:
		messages.error(request,"You don't have the required permissions!")
		return redirect('/login/')
	else:
		messages.error(request,"You are not logged in.")
		return redirect('/login/')
