from django import forms

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)