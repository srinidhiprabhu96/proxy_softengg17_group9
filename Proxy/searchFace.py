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
import logging

log = logging.getLogger('upload_attendance')
hdlr = logging.FileHandler('logfile')
hdlr.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",datefmt="%d/%b/%Y %H:%M:%S")
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.DEBUG)

course_number = sys.argv[1]
date = sys.argv[2]
log.info("Uploading attendance for "+course_number+" on "+date)
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
		log.info("Attendance entries added")
	except:
		log.info("Course not found")
		sys.exit(0)
else:
	log.info("Attendance being updated")

for image in image_paths:
	faces = detectMultipleFaces(image)
	for face in faces:
		log.info("Face token "+face["face_token"]+" found in image")
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
				log.info("Attendance added for "+student.username)
			except:
				row = None
		else:
			log.warning("Face not in course")
			

		

