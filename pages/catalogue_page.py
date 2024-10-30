from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CataloguePage(BasePage, ABC):

    def catalog_page_correct(self):
        self.logger.info(f"{self.class_name}: Catalogue page is correct ")

        assert self.browser.find_element(By.ID, 'product-category').is_displayed()
        assert self.browser.find_element(By.CSS_SELECTOR, 'ul.breadcrumb').is_displayed()
        assert self.browser.find_element(By.CSS_SELECTOR, '#content h2').is_displayed()
        assert self.browser.find_element(By.ID, 'product-list').is_displayed()

        products = self.browser.find_elements(By.CLASS_NAME, 'product-thumb')
        assert len(products) > 4

        assert len(self.browser.find_elements(By.CSS_SELECTOR, 'ul.pagination li'))

    def switch_currency(self, new_currency='EUR'):
        self.logger.info("%s: Switch currency to %s" % (self.class_name, new_currency))

        currency_form = self.browser.find_element(By.CSS_SELECTOR, 'a.dropdown-toggle')
        currency_form.click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.dropdown-menu')))
        self.browser.find_element(By.XPATH, f'//a[@href="{new_currency}"]').click()
        self.wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, 'ul.dropdown-menu')))

    def assert_currency(self, currency):
        self.logger.info("%s: Assert currency is %s" % (self.class_name, currency))

        assert currency in self.browser.find_element(By.CSS_SELECTOR, 'div.dropdown').text
        price_elements = self.browser.find_elements(By.CSS_SELECTOR, 'div.price')
        for el in price_elements:
            assert currency in el.text