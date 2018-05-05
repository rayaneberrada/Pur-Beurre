import requests
import json
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
    products_to_get = {'search_terms':sujet, 'page_size':6, 'page':1, 'json':1}
    request_api_products = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params = products_to_get)
    json = request_api_products.json()
    products = json['products']
    aliments = []
    for product in products:
        aliment = {"name":product['product_name'], "url":product['image_url'], "grade":product['nutrition_grades']}
        aliments.append(aliment)
    print(aliments)
    return render(request, 'aliments_manager/results.html', locals())
