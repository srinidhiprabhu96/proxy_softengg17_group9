from __future__ import unicode_literals

from django.db import models

# Create your models here.



class SignUp(models.Model):
	ACCOUNT_TYPE = (
		('0', 'STUDENT'),
		('1', 'PROFESSOR'),
	)
	name = models.CharField(max_length=30)
	email = models.EmailField(unique=True)
	code = models.CharField(max_length=6)
	account = models.CharField(max_length=1, choices = ACCOUNT_TYPE)
