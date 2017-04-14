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

# This file includes code when a professor uploads photos for taking attendance. A separate process is started, so that the professor can continue to work on his page while the attendance is being recognized. This file is written by Srinidhi.

# Assumption is that the image will be less than 2MB in size. This is because we are using Face++ free.

# Set the logger.
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


atts = Attendance.objects.filter(course_id=course_number,date=date) # Get the attendances

if len(atts) == 0:	# If the attendances are not present, then add the attendance records by setting default to "absent". As the faces are recognized, they will be changed to present.
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

# For each image
for image in image_paths:
	faces = detectMultipleFaces(image)	# Detect the faces and get the face tokens. 
	
	for face in faces:	# Search for each face in the corresponding faceset.
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
			# If face in photo, but not in course, log a warning.
			log.warning("Face not in course")
			

		

