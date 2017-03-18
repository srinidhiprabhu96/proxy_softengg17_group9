from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SignUp(models.Model):
	name = models.CharField(max_length=30)
	email = models.EmailField()
	code = models.CharField(max_length=6)
