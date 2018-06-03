import unittest
from django.test import Client, TestCase
from django.urls import reverse
from aliments_manager.forms import ContactForm

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home_form_valid(self):
        form = ContactForm(data={"sujet":"steak"})
        self.assertTrue(form.is_valid())

    def test_home_form_invalid(self):
        form = ContactForm(data={"sujet":"dsfjnsdofdsfoisdfkosdifjosidjfosdifjosdijfosdifjosdifjosdijfoisdjfosdfoisdfjdsfsdfsdoifdsj"})
        self.assertFalse(form.is_valid())

    def test_home_view_return(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments_manager/index.html')

    def test_registration_view_return(self):
        url = reverse("registration")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments_manager/registration.html')

    def test_conncetion_view_return(self):
        url = reverse("connection")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments_manager/connection.html')

    def test_account_view_return(self):
        url = reverse("account")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments_manager/account.html')

    def test_favorites_view_return(self):
        url = reverse("favorites")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments_manager/favorites.html')

    def test_aliments_view_return(self):
        url = reverse("aliment")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments_manager/aliments.html')

    def test_legalmentions_view_return(self):
        url = reverse("legalmentions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments_manager/legalmentions.html')

    def test_home_view_redirect(self):
        choice = ["redirect", "/results/steak/1"]
        if choice[0] == "redirect":
            response = self.client.get(choice[1], follow=True)
            print(response.request, response.redirect_chain, response.status_code)
            self.assertRedirects(response, "/results/steak/1/", status_code=301)