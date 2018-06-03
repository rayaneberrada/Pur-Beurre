from django.test import TestCase
from aliments_manager.models import Favorites, User
from aliments_manager.functionnalities import Functionnalities


class FavoritesTestCase(TestCase):
    def setUp(self):
        rayane = User.objects.create_user("rayane")
        Favorites.objects.create(user=rayane, url="http.exemple.com", image="fakeImage.png", name="ray", nutriscore="C", code="1234567891012")

    def test_favorite_name(self):
        """Animals that can speak are correctly identified"""
        favorite = Favorites.objects.get(name="ray")
        self.assertEqual(favorite.__str__(), favorite.name)

    def test_getPage(self):
    	display = Functionnalities.getPage("rayane", 1)
    	self.assertEqual(len(display), 1)
