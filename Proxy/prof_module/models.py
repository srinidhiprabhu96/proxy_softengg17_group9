from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=50)
    taught_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_prof")
    taken_by = models.ManyToManyField(User, related_name="%(app_label)s_%(class)s_stud")

# class TrainingData(models.Model):
#     stud = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_stud")
#     image = models.FileField(upload_to='trainingdata')     # extend to many images
#
# def user_directory_path(instance, filename):
#     return 'user_{0}/{1}'.format(instance.user.id, filename)
#
# class AttendancePhotos(models.Model):
#     prof = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_prof")
#     image = models.FileField(upload_to='attendancephotos/'+str(user_directory_path)+'/%Y/%m/%d/')
