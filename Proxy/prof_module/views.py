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

@csrf_exempt
def prof_home(request):
	# add context as third arg to render
	if request.user.is_authenticated() and request.user.is_staff:
		# print request.user.username
		qs = Course.objects.filter(taught_by=request.user)
		return render(request, 'prof_home.html', {'courses':qs})
	elif not request.user.is_staff:
		raise Http404("You don't have the required permissions!")
	else:
		return redirect('/login/')


@csrf_exempt
def prof_course(request, c_id):
	# add context as third arg to render
	if request.user.is_authenticated() and request.user.is_staff:
		try:
			c = Course.objects.get(course_id=c_id,taught_by=request.user)
			return render(request, 'prof_course.html',{'course_id':c_id})
		except Exception as e:
			raise Http404("You don't teach the course!")
	elif not request.user.is_staff:
		raise Http404("You don't have the required permissions!")
	else:
		return redirect('/login/')

# @csrf_exempt
# def add_stud(request, c_id):
# 	# add context as third arg to render
# 	if request.user.is_authenticated:
# 		return render(request, 'add_stud.html')
# 	else:
# 		return redirect('/login/')

# def store_stud: doubt - where to create new student

def daily_report(request, c_id):
	# add context as third arg to render
	return render(request, 'daily_report.html')

def prof_history(request, c_id):
	# add context as third arg to render
	return render(request, 'prof_history.html')

def upload_class_photos(request, c_id):
	if request.user.is_authenticated() and request.user.is_staff:
		return render(request, 'upload_class_photos.html', {'course_id':c_id})
	elif not request.user.is_staff:
		raise Http404("You don't have the required permissions!")
	else:
		return redirect('/login/')

@csrf_exempt
def take_attendance(request, c_id):
	# add context as third arg to render
	if request.user.is_authenticated() and request.user.is_staff and request.method == 'POST':
		form = ClassImagesForm(request.POST, request.FILES)
		if form.is_valid:
			images = request.FILES.getlist('myfiles')
			paths = []
			for i in images:
				# print i.name
				path = default_storage.save(request.user.username+'/'+i.name, ContentFile(i.read()))
				paths += [os.path.join(settings.MEDIA_ROOT, path)]
			messages.success(request, 'Files uploaded successfully!')
		else:
			messages.error(request, 'Unable to upload files. Try again.')
		return redirect('/upload_class_photos/'+c_id+'/')
	elif not request.user.is_staff:
		raise Http404("You don't have the required permissions!")
	elif request.method != 'POST':
		raise Http404("You haven't uploaded any images!")
	else:
		return redirect('/login/')

def prof_queries(request, c_id):
	# add context as third arg to render
	return render(request, 'prof_queries.html')
