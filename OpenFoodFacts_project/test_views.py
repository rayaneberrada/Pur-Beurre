#coding: utf8
import os.path, requests, json, requests_mock

class TestViews:
	def test_getSearch(self):
		test = {
  				"products": [
    				{
      				"product_name": "Spécialité à base de soja",
      				"nutrition_grades": "a",
      				"image_front_url": "https://static.openfoodfacts.org/images/products/327/322/008/6032/front_fr.19.400.jpg",
      				}]
      			}

    	session = requests.Session()
    	adapter = requests_mock.Adapter()
    	session.mount('mock', adapter)
    
    	adapter.register_uri('GET', 'mock://fr.openfoodfacts.org/cgi/search.pl', json=test)
    	resp = session.get('mock://maps.googleapis.com/maps/api/geocode/json?')

    	def mockreturn(request, params):
    	    return resp

    	monkeypatch.setattr(requests, 'get', mockreturn)
    	assert parser.getGeocode("tour eiffel") == test