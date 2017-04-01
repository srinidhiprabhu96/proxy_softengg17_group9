from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Attendance(models.Model):
    course_id = models.CharField(max_length=10)
    date = models.DateTimeField(default=datetime.now, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_stud")
    isPresent = models.BooleanField(default=False)

class Query(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    date = models.DateField(null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_stud")
    text = models.CharField(max_length=1000)
    isApproved = models.BooleanField(default=False)
