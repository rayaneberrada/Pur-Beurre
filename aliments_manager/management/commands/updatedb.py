from django.core.management.base import BaseCommand, CommandError
from aliments_manager.models import Favorites
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        aliments = Favorites.objects.all()
        for aliment in aliments:
            product_to_get = {'code':aliment.code +'.json'}
            product = requests.get('https://fr.openfoodfacts.org/api/v0/produit/', params = product_to_get)
            json = product.json()
            new_aliment = json['product']
            aliment.name = new_aliment['product_name']
            aliment.image = new_aliment['image_thumb_url']
            aliment.nutriscore = new_aliment['nutrition_grades'].upper()
            aliment.save()