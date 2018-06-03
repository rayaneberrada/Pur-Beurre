from django import forms

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=30, label='')

class RegistrationForm(forms.Form):
	nameUser = forms.CharField(max_length=8)
	email = forms.EmailField()
	password = forms.CharField(max_length=12, widget=forms.PasswordInput) 

class ConnectionForm(forms.Form):
	nameUser = forms.CharField(max_length=8)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput) 
	