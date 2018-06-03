import unittest
import requests
import httpretty
import responses
from django.test import Client, TestCase
from django.urls import reverse
from aliments_manager.forms import ContactForm
from aliments_manager.functionnalities import Functionnalities

class SimpleTest(TestCase):
    @httpretty.activate
    def test_getNutrientInfos(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://fr.openfoodfacts.org/api/v0/produit/?code=3259010108078.json",
            body='{"product":{"nutrient_levels": {"saturated-fat":"low"}, "url":"https://fr.openfoodfacts.org/produit/3259010108078", "nutriments":{"saturated-fat_value":"8g"} } }'
        )

        context = Functionnalities.getNutrientInfos("3259010108078")
        print(context)
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(context, {'aliment_selected': {'nutrient_levels': {'saturated': 'low'},\
                                 'url': 'https://fr.openfoodfacts.org/produit/3259010108078', \
                                 'nutriments': {'saturated': '8g'}, 'saturated': 'faible'}, \
                                 'nutrients': {'saturated': 'low'}, 'nutriments': {'saturated': '8g'}})
