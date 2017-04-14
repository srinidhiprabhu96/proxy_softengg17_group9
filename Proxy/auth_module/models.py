from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Model written by Srinidhi, to store the accounts on Signup.
class SignUp(models.Model):
	ACCOUNT_TYPE = (
		('0', 'STUDENT'),
		('1', 'PROFESSOR'),
	)
	STATUS_TYPE = (
		('0', 'NOT_VERIFIED'),
		('1', 'VERIFIED'),
	)
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	code = models.CharField(max_length=32)
	account = models.CharField(max_length=1, choices = ACCOUNT_TYPE)
	status = models.CharField(max_length=1, choices = STATUS_TYPE, default='0')
