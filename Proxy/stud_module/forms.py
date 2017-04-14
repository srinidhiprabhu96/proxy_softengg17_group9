from django import forms

# Form to handle edge cases. Written by Srinidhi
class DateForm(forms.Form):
	date = forms.CharField(required=True)
