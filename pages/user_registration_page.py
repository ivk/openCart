from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage


class UserRegistrationPage(BasePage):

    def open(self, url):
        self.browser.get(f"{self.base_url}{url}")
        WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element(By.TAG_NAME, "main"))
        self.browser.find_element(By.TAG_NAME, 'nav')
        assert self.browser.find_element(By.TAG_NAME, 'header').is_displayed()
        assert len(self.browser.find_elements(By.TAG_NAME, 'footer'))


    def form_exists(self):
        self.browser.find_element(By.CSS_SELECTOR, "main form")
        assert self.browser.find_element(By.CSS_SELECTOR, ".text-end button").is_enabled()