from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

# Model written by Pavan
class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=50)
    taught_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_prof")
    taken_by = models.ManyToManyField(User, related_name="%(app_label)s_%(class)s_stud")

# Model written by Srinidhi
class RollNumberToken(models.Model):
    roll_number = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_stud")
    face_token = models.CharField(max_length=50)
 
# Model written by Srinidhi   
class Facesets(models.Model):
    faceset_token = models.CharField(max_length=50)
    outer_id = models.CharField(max_length=50)

# Model written by Pavan
class Attendance(models.Model):
    IS_PRESENT = (
		('0', 'ABSENT'),
		('1', 'PRESENT'),
	)
    course_id = models.CharField(max_length=10)	# Use foreign key if possible
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_stud")
    prof = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_prof")
    date = models.DateField(default=datetime.date.today)	# Date is a string of the form YYYY-MM-DD
    is_present = models.CharField(max_length=1, choices = IS_PRESENT, default='0')
    
    class Meta:		# This is included to make the row unique w.r.t course_id, student and date taken together.
    	unique_together = ('course_id', 'student', 'date',)

# Model written by Pavan
class Query(models.Model):
    STATUS = (
		('0', 'IN PROGRESS'),
		('1', 'ACCEPTED'),
		('2', 'DECLINED'),
	)
    course_id = models.CharField(max_length=10)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_stud")
    date = models.DateField(default=datetime.date.today)
    query = models.CharField(max_length=500)
    status = models.CharField(max_length=1, choices = STATUS, default='0')

