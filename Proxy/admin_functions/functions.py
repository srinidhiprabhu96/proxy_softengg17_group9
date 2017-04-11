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
	count = 0
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
					print "Token saved " + str(count)
					count += 1 
			except:
				print "No user found for "+image
				pass

def addFacesToFaceSet():
	courses = Course.objects.all()
	for course in courses:
		students = course.taken_by.all()
		#print students
		count = 0
		for student in students:
			try:
				row = RollNumberToken.objects.get(roll_number=student)
				addFaceSet(course.course_id,[row.face_token])
				print "Face added to faceset "+str(count)
				count += 1
			except:
				print "Student's face token not found"
				pass

# Add student whose email is 'stud_email' to the course with course ID 'courseId' which is taught by the prof whose email is 'prof_email'
# assuming that student, course and prof are present in the database
def studAddCourse(stud_email, courseId, prof_email):
	s = User.objects.get(email=stud_email)
	p = User.objects.get(email=prof_email)
	c = Course.objects.get(course_id=courseId, taught_by=p)
	try:
		c.taken_by.add(s)
		c.save()
	except:
		pass

# Create course which taken by the prof
# assuming that prof is present in the database
def profCreateCourse(prof_email, courseId, courseTitle):
	p = User.objects.get(email=prof_email)
	c = Course.objects.create(course_id=courseId,course_name=courseTitle,taught_by=p)

def addCS14studentsToCourse():
	for i in range(1,63):
		if i < 10:
			studAddCourse("cs14b00"+str(i)+"@smail.iitm.ac.in","CS1400","prof@iitm.ac.in")
		else:
			studAddCourse("cs14b0"+str(i)+"@smail.iitm.ac.in","CS1400","prof@iitm.ac.in")
			
def createUser(stud_name,stud_email):
	try:
		u = User.objects.create(first_name=stud_name,email=stud_email,username=stud_email,is_staff="0")
		u.set_password("123567")
		u.save()
	except:
		pass
			
def createCS14Users():
	for i in range(1,63):
		if i < 10:
			createUser("CS14B00"+str(i),"cs14b00"+str(i)+"@smail.iitm.ac.in")
		else:
			createUser("CS14B0"+str(i),"cs14b0"+str(i)+"@smail.iitm.ac.in")
createFaceSet("CS1400")
#createFaceSet("CS3420")
# createFaceSetForCourses()
#UploadTrainingData("TrainingData")
addFacesToFaceSet()

#createCS14Users()
#profCreateCourse('prof@iitm.ac.in','CS1400','CS new course')
#addCS14studentsToCourse()
# studAddCourse('stud1@smail.iitm.ac.in','CS1400', 'prof@iitm.ac.in')
# studAddCourse('stud2@smail.iitm.ac.in','CS1400', 'prof@iitm.ac.in')
