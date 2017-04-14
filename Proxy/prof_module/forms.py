from django import forms

# Form to get the uploaded images during take attendance. Written by Pavan.
class ClassImagesForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    date = forms.CharField()
