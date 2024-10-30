"""
Часть 2
2.1 Написать тесты проверяющие элементарное наличие элементов на разных страницах приложения opencart
2.2 Реализовать минимум пять тестов (одни тест = одна страница приложения)
2.3 Использовать методы явного ожидания элементов

Покрыть нужно:

Главную
Каталог
Карточку товара
Страницу логина в админку /administration
Страницу регистрации пользователя (/index.php?route=account/register)
Какие именно элементы проверять определить самостоятельно, но не меньше 5 для каждой страницы
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.user_registration_page import UserRegistrationPage
from pages.admin_login_page import AdminPage
from pages.goods_card_page import CardPage
from pages.catalogue_page import CataloguePage
from pages.main_page import MainPage

TIMEOUT = 1


def test_main(browser, base_url):
    page = MainPage(base_url, browser, TIMEOUT)
    page.open("/")
    page.fulfill()


def test_catalogue(browser, base_url):
    catalogue = CataloguePage(base_url, browser, TIMEOUT)
    catalogue.open("/catalog/desktops")
    catalogue.catalog_page_correct()


def test_card(browser, base_url):
    card = CardPage(base_url, browser, TIMEOUT)
    card.open("/product/desktops/macbook")
    card.cards_correct()


def test_admin_login_page(browser, base_url):
    admin_login = AdminPage(base_url, browser, TIMEOUT)
    admin_login.open("/administration")
    admin_login.form_exists_and_correct()


def test_user_registration(browser, base_url):
    user_reg_page = UserRegistrationPage(base_url, browser, TIMEOUT)
    user_reg_page.open("/?route=account/register")
    user_reg_page.form_exists()