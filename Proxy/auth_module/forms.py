from django import forms

# Froms writen by Srinidhi for handling edge cases in auth_module
class SignUpForm(forms.Form):
	name = forms.CharField()
	email = forms.EmailField()

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField()
