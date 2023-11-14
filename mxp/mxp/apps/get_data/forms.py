from django import forms

class UserForm(forms.Form):
    address = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    port = forms.CharField(max_length=100)