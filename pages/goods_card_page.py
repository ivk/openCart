from abc import ABC

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage

class CardPage(BasePage, ABC):

    @allure.step("Product card is correct")
    def cards_correct(self):
        self.logger.info(f"{self.class_name}: Product card is correct")

        assert self.browser.find_element(By.CSS_SELECTOR, '#product-info #content').is_displayed()
        assert self.browser.find_element(By.TAG_NAME, 'h1').is_displayed()
        price = self.browser.find_element(By.CLASS_NAME, 'price-new').text
        assert '$' in price
        assert float(price[1:]) > 100