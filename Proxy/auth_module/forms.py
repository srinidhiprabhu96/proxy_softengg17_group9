from django import forms

class SignUpForm(forms.Form):
	name = forms.CharField()
	email = forms.EmailField()

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField()
