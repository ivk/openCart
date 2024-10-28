from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

class MainPage(BasePage):

    def open(self, url):
        self.logger.debug("%s: Opening url: %s" % (self.class_name, url))
        self.browser.get(f"{self.base_url}")
        assert WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element(By.TAG_NAME, "footer"))

    def fulfill(self):
        assert "Your Store" in self.browser.title
        assert self.browser.find_element(By.ID, "logo").is_displayed()

        product_cards = self.browser.find_elements(By.CLASS_NAME, "product-thumb")
        assert len(product_cards) == 4

        assert self.browser.find_element(By.ID, "carousel-banner-1").is_displayed()
        assert "OpenCart" in self.browser.find_element(By.TAG_NAME, "footer").text