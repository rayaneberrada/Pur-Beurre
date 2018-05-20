import requests
import json

class Functionnalities(object):
    """docstring for Functionnalities"""
    def getSearch(product_to_search):
        products_to_get = {'search_terms':product_to_search, 'page_size':12,'json':1}
        request_api_products = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params = products_to_get)
        json = request_api_products.json()
        products = json['products']
        return products
