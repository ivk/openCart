from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CataloguePage(BasePage):

    def open(self, url):
        self.browser.get(f"{self.base_url}{url}")
        assert WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element(By.TAG_NAME, "main"))

    def catalog_page_correct(self):
        assert self.browser.find_element(By.ID, 'product-category').is_displayed()
        assert self.browser.find_element(By.CSS_SELECTOR, 'ul.breadcrumb').is_displayed()
        assert self.browser.find_element(By.CSS_SELECTOR, '#content h2').is_displayed()
        assert self.browser.find_element(By.ID, 'product-list').is_displayed()

        products = self.browser.find_elements(By.CLASS_NAME, 'product-thumb')
        assert len(products) > 4

        assert len(self.browser.find_elements(By.CSS_SELECTOR, 'ul.pagination li'))

    def switch_currency(self, new_currency='EUR'):
        currency_form = self.browser.find_element(By.CSS_SELECTOR, 'a.dropdown-toggle')
        currency_form.click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.dropdown-menu')))
        self.browser.find_element(By.XPATH, f'//a[@href="{new_currency}"]').click()
        self.wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, 'ul.dropdown-menu')))

    def assert_currency(self, currency):
        assert currency in self.browser.find_element(By.CSS_SELECTOR, 'div.dropdown').text
        price_elements = self.browser.find_elements(By.CSS_SELECTOR, 'div.price')
        for el in price_elements:
            assert currency in el.text