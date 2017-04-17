from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from auth_module.models import *
from prof_module.models import *
from stud_module.models import *
import datetime

# This file is written by Pavan.

prof = User(username='prof@iitm.ac.in',first_name='Prof',email='prof@iitm.ac.in',password=make_password('123567'),is_staff=True)
prof.save()
s1 = User(username='stud1@smail.iitm.ac.in',first_name='Student1',email='stud1@smail.iitm.ac.in',password=make_password('123567'),is_staff=False)
s2 = User(username='stud2@smail.iitm.ac.in',first_name='Student2',email='stud2@smail.iitm.ac.in',password=make_password('123567'),is_staff=False)
s1.save()
s2.save()

c1 = Course(course_id='CS1100',course_name='C programming',taught_by=prof,taken_by=[s1,s2])
c2 = Course(course_id='CS1300',course_name='Intro to CSE',taught_by=prof,taken_by=[s1,s2])
c1.save()
c2.save()

a1 = Attendance(course_id='CS1100',student=s1,prof=prof,is_present='0',date=datetime.date(2017,4,1))
a2 = Attendance(course_id='CS1100',student=s2,prof=prof,is_present='1',date=datetime.date(2017,4,2))
a3 = Attendance(course_id='CS1300',student=s1,prof=prof,is_present='1')
a4 = Attendance(course_id='CS1300',student=s2,prof=prof,is_present='0')
a1.save()
a2.save()

a3.save()
a4.save()

c1 = Course.objects.get(course_id="CS1100")
s = User.objects.filter(is_staff=False)
"""
a = User.objects.get(username="cs14b028@smail.iitm.ac.in")
print a
c1.taken_by.add(a)
c1.save()
c1 = Course.objects.get(course_id="CS1100")
print c1.taken_by.all()
a.save()
c1 = Course(course_id='CS2100',course_name='DM',taught_by=a,taken_by=[a])
c1.save()
print c1.taken_by
"""
#print s
"""
for i in range(0,len(s)):
	print i
	c1.taken_by.add(s[i])
	print c1.taken_by
	c1.save()
#c1.taken_by = s
print c1.taken_by.all()
c1.save()
"""

q1 = Query(course_id='CS1100',student=s1,status='0',date=datetime.date(2017,4,1),query='some query')
q2 = Query(course_id='CS1100',student=s2,status='1',date=datetime.date(2017,4,2),query='some query 2')
q1.save()
q2.save()
