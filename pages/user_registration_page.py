from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage


class UserRegistrationPage(BasePage, ABC):

    def form_exists(self):
        self.logger.info(f"{self.class_name}: User registration is possible")

        self.browser.find_element(By.CSS_SELECTOR, "main form")
        assert self.browser.find_element(By.CSS_SELECTOR, ".text-end button").is_enabled()