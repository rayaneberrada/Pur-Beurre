from django import forms

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)

class RegistrationForm(forms.Form):
	nameUser = forms.CharField(max_length=8)
	email = forms.CharField(max_length=40)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput) 

class ConnectionForm(forms.Form):
	nameUser = forms.CharField(max_length=8)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput) 
	