from django.shortcuts import render
from .forms import ContactForm

# Create your views here.
def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    form = ContactForm(request.POST or None)
    if form.is_valid(): 
    	succes = True 
    return render(request, 'aliments_manager/index.html', locals())