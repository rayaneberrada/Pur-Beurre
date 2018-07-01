import requests
import json
from .forms import ContactForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from aliments_manager.models import Favorites
from django.core.paginator import Paginator, EmptyPage
from operator import itemgetter


class Functionnalities(object):
    """Functionnalities used by the views"""
    @staticmethod
    def getSearch(product_to_search):
        """
        Get the products from the OpenFoodFacts API and return a dictionnary of them depending
        of the user search
        """
        products_to_get = {'search_terms':product_to_search, 'page_size':100,'json':1}
        request_api_products = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params = products_to_get)
        json = request_api_products.json()
        products = json['products']
        #return products

    @staticmethod
    def getAliment(code):
        """
        Get the nutritionnal informations of an aliment via the OpenFoodFact API using the code of the aliment
        selected
        """
        products_to_get = {'code':code+'.json'}
        request_api_products = requests.get('https://fr.openfoodfacts.org/api/v0/produit/', params = products_to_get)
        json = request_api_products.json()
        aliment = json['product']
        return aliment

    @staticmethod
    def searchFormValid(request):
        """
        Check if the informations sent by the user are valid an return the redirection address or the 
        form to display if the informations are not valid
        """
        searchForm = ContactForm(request.POST or None)
        if searchForm.is_valid():
            aliment = searchForm.cleaned_data['sujet']
            page_id = 1
            url = reverse("results", kwargs={"aliment_searched":aliment, "page_id":page_id})
            return ["redirect", url]
        else:
            return [searchForm]

    @staticmethod
    def chosePage(aliments, page_id):
        """
        Return the page to display with the aliments contained inside
        """
        paginator = Paginator(aliments, 6)
        try:
            page = paginator.page(page_id)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page

    @staticmethod
    def updateSession(request):
        """
        Set the previous_seesion variable that will contain the last search made
        """
        if 'session_name' in request.session:
            previous_session = request.session['session_name']
        else:
            previous_session = ""
        return previous_session

    @staticmethod
    def getAlimentsFromAPI(request, previous_session, aliment_searched, page_id):
        """
        This function clean the data received from the API to keep only the usefull informations
        and return the context for the results view template containing a dictionnary of the aliments 
        found on OpenFoodFacts, the image of the worst aliment corresponding to the search and the 
        value searched
        """
        aliments = []

        if previous_session == aliment_searched:
                aliments = request.session['aliment_session']
                first_image = request.session['first_image']
        else:
            products = Functionnalities.getSearch(aliment_searched)
            first_image = ""
            for product in products:
                if 'nutrition_grades' in product and 'image_url' in product and 'codes_tags' in product:
                    if len(str(product['codes_tags'][1])) == 13 and product['nutrition_grades'] in ["a", "b", "c"] :
                        aliment = {"name":product['product_name'], "url_image":product['image_url'],\
                                 "grade":product['nutrition_grades'], "code":str(product['codes_tags'][1]),\
                                 "nutrient_levels":product['nutrient_levels'], "nutriments":product['nutriments'],\
                                 "url":product["url"]}
                        aliments.append(aliment)
                    elif len(str(product['codes_tags'][1])) == 13 and product['nutrition_grades'] in ["d","e"] and first_image == "":
                        first_image = {"name":product['product_name'], "url_image":product['image_url']}
                        request.session['first_image'] = first_image
            aliments = sorted(aliments, key=itemgetter('grade'))

        request.session['aliment_session'] = aliments
        request.session['session_name'] = aliment_searched

        pageToDisplay = Functionnalities.chosePage(aliments, page_id)
        context = {"aliments":pageToDisplay, "firstAliment":first_image, "aliment_searched":aliment_searched}
        return context

    @staticmethod
    def getNutrientInfos(code):
        """
        Organise the informations that will be displayed on the page describing the aliment selected
        """
        aliment_selected = Functionnalities.getAliment(code[:13])
        nutrients = aliment_selected['nutrient_levels']
        nutriments = aliment_selected['nutriments']
        nutriments['saturated'] = nutriments.pop('saturated-fat_value')
        aliment_selected['nutrient_levels']['saturated'] = aliment_selected['nutrient_levels'].pop('saturated-fat')
        aliment_selected['url'] = "https://fr.openfoodfacts.org/produit/"+code
        for level in nutrients:
            if nutrients[level] == "low":
                aliment_selected[level] = 'faible'
            elif nutrients[level] == "moderate":
                aliment_selected[level] = 'modérée'
            elif nutrients[level] == "high":
                aliment_selected[level] = 'élevée'

        context = {"aliment_selected":aliment_selected, "nutrients":nutrients, "nutriments":nutriments}
        return context

    @staticmethod
    def getPage(username, page_id):
        """
        Return the page with aliments corresponding to display
        """
        user = User.objects.get(username=username)
        aliments = Favorites.objects.filter(user=user)
        paginator = Paginator(aliments, 6)
        try:
            display = paginator.page(page_id)
            return display
        except EmptyPage:
            display = paginator.page_id(paginator.num_pages)
            return display

    @staticmethod
    def checkSessionExist():
        """
        Check that the session correspond to the search made
        """
        if 'session_name' in request.session:
            previous_session = request.session['session_name']
        else:
            previous_session = ""

        if previous_session == aliment_searched:
            aliments = request.session['aliment_session']
            first_image = request.session['first_image']
            print("j'utilise une session")