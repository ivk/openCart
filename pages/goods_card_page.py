from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage

class CardPage(BasePage):

    def open(self, url):
        self.browser.get(f"{self.base_url}{url}")
        assert WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element(By.TAG_NAME, "main"))


    def cards_correct(self):
        assert self.browser.find_element(By.CSS_SELECTOR, '#product-info #content').is_displayed()
        assert self.browser.find_element(By.TAG_NAME, 'h1').is_displayed()
        price = self.browser.find_element(By.CLASS_NAME, 'price-new').text
        assert '$' in price
        assert float(price[1:]) > 100