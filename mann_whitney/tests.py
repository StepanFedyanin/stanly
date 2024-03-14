from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class MySeleniumTests(StaticLiveServerTestCase):
    url_account_login = 'http://localhost/all/accounts/login/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        firefox_profile_path = "/home/jenia0jenia/.mozilla/firefox/pii69owz.default"
        cls.selenium = webdriver.Firefox(firefox_profile_path)
        # cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(self.url_account_login)
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('jenia0jenia@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('4ernenk0')
        remember_checkbox = self.selenium.find_element_by_xpath('//label[@for="id_remember"]')
        remember_checkbox.click()
        self.selenium.find_element_by_xpath('//input[@value="Войти"]').click()
        # print(remember_checkbox.get_attribute('value'))

    def test_login_vk(self):
        self.selenium.get(self.url_account_login)
        self.selenium.find_element_by_css_selector('.popup-form__social.socialaccount_provider').click()
