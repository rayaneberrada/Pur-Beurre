import requests
import json
from .functionnalities import Functionnalities
from django.shortcuts import render
from .forms import ContactForm


# Create your views here.
def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    form = ContactForm(request.POST or None)
    if form.is_valid(): 
    	succes = True 
    return render(request, 'aliments_manager/index.html', locals())

def results(request):
    form = ContactForm(request.POST or None)
    if form.is_valid(): 
    	succes = True 
    	sujet = form.cleaned_data['sujet']
    products = Functionnalities.getSearch(sujet)
    aliments = []
    firstAliment = False
    for product in products:
        if 'nutrition_grades' in product and 'image_url' in product:
            if firstAliment != False:
                aliment = {"name":product['product_name'], "url":product['image_url'], "grade":product['nutrition_grades']}
                aliments.append(aliment)
            else:
                firstAliment  = product['image_url']
    return render(request, 'aliments_manager/results.html', locals())
