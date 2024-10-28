from abc import ABC, abstractmethod
import random
import logging

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, base_url, browser,  timeout):
        self.timeout = timeout
        self.browser = browser
        self.base_url = base_url
        self.wait = WebDriverWait(browser, timeout)

        self.logger = browser.logger
        self.class_name = type(self).__name__

    @abstractmethod
    def open(self, url):
        self.logger.debug("%s: Opening url: %s" % (self.class_name, url))
        self.browser.get(f"{self.base_url}{url}")
        assert self.browser.find_element(By.TAG_NAME, 'header').is_displayed()
        assert self.browser.find_element(By.TAG_NAME, 'footer').is_displayed()

    def scroll_to_element(self, el, x=0, y=1000):
        actions = ActionChains(self.browser)

        actions.scroll_by_amount(x, y).perform()
        actions.scroll_to_element(el)
        self.wait.until(EC.visibility_of(el))
        return el


    def put_rand_to_shopping_cart(self, rand=4):
        shopping_cart_icon = self.browser.find_element(By.CLASS_NAME, 'fa-cart-shopping')
        assert '0 item', shopping_cart_icon.text

        indx = random.randint(1, rand)
        xpath = f"(//div[@class='button-group']/button[1])[{indx}]"
        el = self.browser.find_element(By.XPATH, xpath)
        self.scroll_to_element(el).click()

        self.wait.until(EC.presence_of_element_located((By.ID, 'alert')))
        assert '1 item', shopping_cart_icon.text