from abc import ABC

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class MainPage(BasePage, ABC):

    @allure.step("Main page is correct")
    def fulfill(self):
        self.logger.info(f"{self.class_name}: Main page is ok ")

        assert "Your Store" in self.browser.title
        assert self.browser.find_element(By.ID, "logo").is_displayed()

        product_cards = self.browser.find_elements(By.CLASS_NAME, "product-thumb")
        assert len(product_cards) == 4

        assert self.browser.find_element(By.ID, "carousel-banner-1").is_displayed()
        assert "OpenCart" in self.browser.find_element(By.TAG_NAME, "footer").text