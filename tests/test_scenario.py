"""
Часть 3
"""
import random
from curses import has_key

import pytest
from selenium.webdriver.common.by import By
import time
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from conftest import browser

TIMEOUT = 10
USERNAME = 'user'
PASSWORD = 'bitnami'

def switch_currency(browser, new_currency='EUR'):
    wait = WebDriverWait(browser, TIMEOUT)

    currency_form = browser.find_element(By.CSS_SELECTOR, 'a.dropdown-toggle')
    currency_form.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.dropdown-menu')))
    browser.find_element(By.XPATH, f'//a[@href="{new_currency}"]').click()
    wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, 'ul.dropdown-menu')))

    return True

def scroll_to_element(browser, el):
    actions = ActionChains(browser)
    wait = WebDriverWait(browser, TIMEOUT)

    actions.scroll_by_amount(0, 1000).perform()
    actions.scroll_to_element(el)
    wait.until(EC.visibility_of(el))

    return el

def test_admin_login(browser, base_url):
    """
    3.1 Написать автотест логина-разлогина в админку с проверкой, что логин был выполнен
    """
    browser.get(f"{base_url}/administration")

    wait = WebDriverWait(browser, TIMEOUT)
    content = browser.find_element(By.ID, "content")

    # logged out
    assert "Administration" in browser.title
    assert "Please enter your login details." in content.text

    browser.find_element(By.NAME, "username").send_keys(USERNAME)
    browser.find_element(By.NAME, "password").send_keys(PASSWORD)
    browser.find_element(By.TAG_NAME, 'button').click()

    el = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

    assert 'Dashboard' == el.text
    assert 'John Doe' in browser.find_element(By.ID, 'nav-profile').text

    browser.find_element(By.CSS_SELECTOR, '#nav-logout a').click()
    wait.until(EC.url_changes('/administration/index.php?route=common/login'))
    assert "Administration" in browser.title
    assert browser.find_element(By.ID, 'form-login')


def test_put_something_into_basket(browser, base_url):
    """
    3.2 Добавить в корзину случайный товар с главной страницы и проверить что он появился в корзине
    """
    browser.get(base_url)

    wait = WebDriverWait(browser, TIMEOUT)
    shopping_cart_icon = browser.find_element(By.CLASS_NAME, 'fa-cart-shopping')

    assert '0 item', shopping_cart_icon.text

    indx = random.randint(1,4)
    xpath = f"(//div[@class='button-group']/button[1])[{indx}]"
    el = browser.find_element(By.XPATH, xpath)
    scroll_to_element(browser, el).click()

    wait.until(EC.presence_of_element_located((By.ID, 'alert')))
    assert '1 item', shopping_cart_icon.text

@pytest.mark.parametrize("url", ("/", "/catalog/smartphone"))
def test_switch_currency(browser, base_url, url):
    """
    3.3 Проверить, что при переключении валют цены на товары меняются на главной
    3.4 Проверить, что при переключении валют цены на товары меняются в каталоге
    """
    wait = WebDriverWait(browser, TIMEOUT)
    browser.get(base_url+url)

    switch_currency(browser, 'EUR')
    assert '€' in browser.find_element(By.CSS_SELECTOR, 'div.dropdown').text
    price_elements = browser.find_elements(By.CSS_SELECTOR, 'div.price')
    for el in price_elements:
        assert '€' in el.text

    switch_currency(browser, 'USD')
    assert '$' in browser.find_element(By.CSS_SELECTOR, 'div.dropdown').text
    price_elements = browser.find_elements(By.CSS_SELECTOR, 'div.price')
    for el in price_elements:
        assert '$' in el.text
