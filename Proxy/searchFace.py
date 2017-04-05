# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Proxy.settings")
django.setup()
import datetime
from prof_module.api_wrappers import *
from prof_module.models import *
from django.contrib.auth.models import User

course_number = sys.argv[1]
date = sys.argv[2]
image_paths = sys.argv[3:]
date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
#print image_paths
"""
course_number = "CS1100"
row_course = Course.objects.get(course_id=course_number)
prof = row_course.taught_by
stud1 = row_course.taken_by.all()[0]
a = Attendance(course_id=course_number,student=stud1,prof=prof,is_present="1")
a.save()
"""
atts = Attendance.objects.filter(course_id=course_number,date=date)
if len(atts) == 0:
	try:
		course = Course.objects.get(course_id=course_number)
		students_in_course = course.taken_by.all()
		for student in students_in_course:
			a = Attendance(course_id=course.course_id,prof=course.taught_by,student=student,date=date)
			a.save()
		print "Attendance entries added"
	except:
		print "Course not found"
		sys.exit(0)
else:
	print "Attendance being updated"

for image in image_paths:
	faces = detectMultipleFaces(image)
	for face in faces:
		print face["face_token"]
		response = searchFace(course_number,face_token=face["face_token"])
		if response["results"][0]["confidence"] > 65.3:	# 65.3 is the threshold for error
			token = response["results"][0]["face_token"]
			try:
				row = RollNumberToken.objects.get(face_token=token)
				student = row.roll_number
				row_course = Course.objects.get(course_id=course_number)
				prof = row_course.taught_by
				a = Attendance.objects.get(course_id=course_number,student=student,date=date)
				a.is_present="1"
				a.save()
				print "Attendance added"
			except:
				row = None
		else:
			print "Face not in course"
			

		

