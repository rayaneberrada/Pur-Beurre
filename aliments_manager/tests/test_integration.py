from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
import time


class MySeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def test_user_creation(self):
        connection_page = self.browser.find_element_by_id('account')
        connection_page.click()
        registration_page = self.browser.find_element_by_xpath('//a[@href="/registration/"]')
        registration_page.click()

        username_registration = self.browser.find_element_by_id('id_nameUser')
        username_registration.send_keys('seletest')
        username_email = self.browser.find_element_by_id('id_email')
        username_email.send_keys('seletest@gmail.com')
        password_registration = self.browser.find_element_by_id('id_password')
        password_registration.send_keys('1234')
        password_registration.submit()

        check_form_present =  WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "accountCreation")))
        username_connection = self.browser.find_element_by_name('nameUser')
        username_connection.send_keys('seletest')
        password_connection = self.browser.find_element_by_name('password')
        password_connection.send_keys('1234')
        password_connection.submit()

        check_homePage =  WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h2")))
        connected = self.browser.find_element_by_xpath('//h2')
        self.assertIn('Vous êtes bien connecté', connected.text)
        self.browser.quit()

    def test_search(self):
        elem = self.browser.find_element_by_id('id_sujet')
        elem.send_keys('steak')
        elem.submit()
        self.browser.implicitly_wait(15)
        products = self.browser.find_elements_by_xpath('//div[@class="col-sm-4 text-center"]')
        error_msg = self.browser.find_element_by_xpath('//h3')

        if error_msg.text == "Il n'existe pas d'aliments sains pour la recherche que vous avez effectué":
            self.assertIn(error_msg.text,"Il n'existe pas d'aliments sains pour la recherche que vous avez effectué")
        else:
            self.assertNotEqual(len(products), 0)
        self.browser.quit()

    def test_add_to_favorites(self):
        connection_page = self.browser.find_element_by_id('account')
        user_test = User.objects.create_user("test_use", "test@gmail.com", "test")
        check_user = User.objects.all()

        connection_page = self.browser.find_element_by_id('account')
        connection_page.click()
        username_connection = self.browser.find_element_by_name('nameUser')
        username_connection.send_keys("test_use")
        password_connection = self.browser.find_element_by_name('password')
        password_connection.send_keys('test')
        password_connection.submit()
        check_homePage =  WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h2")))

        elem = self.browser.find_element_by_id('id_sujet')
        elem.send_keys('steak')
        elem.submit()

        check_resultsPage =  WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "aliment_image")))
        product = self.browser.find_elements_by_css_selector('.svg-inline--fa')
        product[6].click()
        check_ajax_over =  WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "message")))

        favorite_page = self.browser.find_element_by_id('carrot')
        favorite_page.click()
        favorites = self.browser.find_elements_by_xpath('//div[@class="col-sm-4 text-center"]')
        self.assertNotEqual(len(favorites), 0)
        self.browser.quit()


