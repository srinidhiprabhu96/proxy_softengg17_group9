from django import forms

class SignUpForm(forms.Form):
	name = forms.CharField()
	email = forms.EmailField()
