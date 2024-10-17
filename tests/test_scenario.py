"""
Часть 3
"""
import random
from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from conftest import browser

from pages.admin_login_page import AdminPage
from pages.base_page import BasePage
from pages.catalogue_page import CataloguePage
from pages.main_page import MainPage

TIMEOUT = 10
USERNAME = 'user'
PASSWORD = 'bitnami'


def test_admin_login(browser, base_url):
    """
    3.1 Написать автотест логина-разлогина в админку с проверкой, что логин был выполнен
    """
    page = AdminPage(base_url, browser, TIMEOUT)
    content = page.open("/administration")
    page.is_unauthorized(content)
    page.form_exists_and_correct()
    page.login(USERNAME, PASSWORD)
    page.logout()


@pytest.mark.parametrize(["url", "rand"], {("/", 4), ("/catalog/component/monitor", 2)})
def test_put_something_into_basket(browser, base_url, url, rand):
    """
    3.2 Добавить в корзину случайный товар с главной страницы и проверить что он появился в корзине
    """
    page = BasePage(base_url, browser, TIMEOUT)
    page.open(url)
    page.put_rand_to_shopping_cart(2)


@pytest.mark.parametrize("url", ("/", "/catalog/smartphone"))
def test_switch_currency(browser, base_url, url):
    """
    3.3 Проверить, что при переключении валют цены на товары меняются на главной
    3.4 Проверить, что при переключении валют цены на товары меняются в каталоге
    """
    page = CataloguePage(base_url, browser, TIMEOUT)
    page.open(url)
    page.switch_currency('EUR')
    page.assert_currency('€')
    page.switch_currency('USD')
    page.assert_currency('$')

# Добавление нового товара в разделе администратора
def test_add_product(browser, base_url):
    page = AdminPage(base_url, browser, TIMEOUT)
    page.open()
    page.login(USERNAME, PASSWORD)
    page.add_product('test', 'a-6', 'test-a6')

