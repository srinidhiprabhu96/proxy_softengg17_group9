from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=50)
    taught_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_prof")
    taken_by = models.ManyToManyField(User, related_name="%(app_label)s_%(class)s_stud")
    
class RollNumberToken(models.Model):
    roll_number = models.CharField(max_length=10)
    face_token = models.CharField(max_length=50)
    
class Attendance(models.Model):
    IS_PRESENT = (
		('0', 'ABSENT'),
		('1', 'PRESENT'),
	)
    course_id = models.CharField(max_length=10)	# Use foreign key if possible
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_stud")
    date = models.DateField(null=True)	# Date is a string of the form YYYY-MM-DD
    is_present = models.CharField(max_length=1, choices = IS_PRESENT, default='0')
    
class Query(models.Model):
    STATUS = (
		('0', 'IN PROGRESS'),
		('1', 'ACCEPTED'),
		('2', 'DECLINED'),
	)
    course_id = models.CharField(max_length=10)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_stud")
    date = models.DateField(null=True)
    query = models.CharField(max_length=500)
    status = models.CharField(max_length=1, choices = STATUS, default='0')
    
