from prof_module.api_wrappers import *
from prof_module.models import *
from django.contrib.auth.models import User
import os

# To run this script
# 1) python manage.py shell
# 2) execfile("<path>/functions.py")
# To create facesets for courses that do not already have a faceset
def createFaceSetForCourses():
	courses = Course.objects.all()
	course_list = []
	for item in courses:
		course_list.append(item.course_id)
	facesets = Facesets.objects.all()
	outer_ids = []
	for item in facesets:
		outer_ids.append(item.outer_id)
	#print course_list
	#print outer_ids
	to_create = list(set(course_list) - set(outer_ids))
	print to_create
	for item in to_create:
		createFaceSet(item)
	print "Created required facesets"

# Assumption is that the images will be stored in the TrainingData folder and the files will be named <roll_no.>.jpg. path is the path to the training data folder
def UploadTrainingData(path):
	images = os.listdir(path)
	for image in images:
		if "jpg" in image or "png" in image:	# Only these 2 formats are allowed
			user = image.lower().replace(".jpg","") + "@smail.iitm.ac.in"
			#print user
			try:
				user_obj = User.objects.get(username=user)
				try:
					RollNumberToken.objects.get(roll_number=user_obj)	# If the face token is already there in the table, we don't do anything
					print "Token for "+user+" already present"
				except:
					print "Getting token for "+user
					token = detectFace(path+"/"+image)
					r = RollNumberToken(roll_number=user_obj,face_token=token)
					r.save()
					print "Token saved"
			except:
				print "No user found for "+image
				pass

def addFacesToFaceSet():
	courses = Course.objects.all()
	for course in courses:
		students = course.taken_by.all()
		#print students
		for student in students:
			try:
				row = RollNumberToken.objects.get(roll_number=student)
				addFaceSet(course.course_id,[row.face_token])
				print "Face added to faceset"
			except:
				print "Student's face token not found"
				pass

# Add student whose email is 'stud_email' to the course with course ID 'courseId' which is taught by the prof whose email is 'prof_email'
# assuming that student, course and prof are present in the database
def studAddCourse(stud_email, courseId, prof_email):
	s = User.objects.get(email=stud_email)
	p = User.objects.get(email=prof_email)
	c = Course.objects.get(course_id=courseId, taught_by=p)
	c.taken_by.add(s)
	c.save()

# Create course which taken by the prof
# assuming that prof is present in the database
def profCreateCourse(prof_email, courseId, courseTitle):
	p = User.objects.get(email=prof_email)
	c = Course.objects.create(course_id=courseId,course_name=courseTitle,taught_by=p)


#createFaceSet("CS3420")
# createFaceSetForCourses()
# UploadTrainingData("TrainingData")
# addFacesToFaceSet()

# profCreateCourse('prof@iitm.ac.in','CS1400','Course Title')
# studAddCourse('stud1@smail.iitm.ac.in','CS1400', 'prof@iitm.ac.in')
# studAddCourse('stud2@smail.iitm.ac.in','CS1400', 'prof@iitm.ac.in')
