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
import allure
from allure_commons.types import Severity

from pages.user_registration_page import UserRegistrationPage
from pages.admin_login_page import AdminPage
from pages.goods_card_page import CardPage
from pages.catalogue_page import CataloguePage
from pages.main_page import MainPage

TIMEOUT = 1


@allure.severity(severity_level=Severity.BLOCKER)
@allure.title("Main page checking")
@allure.feature("Pages testing")
def test_main(browser, base_url):
    page = MainPage(base_url, browser, TIMEOUT)
    page.open("/")
    page.fulfill()


@allure.severity(severity_level=Severity.NORMAL)
@allure.title("Catalogue page checking")
@allure.feature("Pages testing")
def test_catalogue(browser, base_url):
    catalogue = CataloguePage(base_url, browser, TIMEOUT)
    catalogue.open("/catalog/desktops")
    catalogue.catalog_page_correct()


@allure.severity(severity_level=Severity.NORMAL)
@allure.title("Product page checking")
@allure.feature("Pages testing")
def test_card(browser, base_url):
    card = CardPage(base_url, browser, TIMEOUT)
    card.open("/product/desktops/macbook")
    card.cards_correct()


@allure.severity(severity_level=Severity.MINOR)
@allure.title("Admin page login checking")
@allure.feature("Pages testing")
def test_admin_login_page(browser, base_url):
    admin_login = AdminPage(base_url, browser, TIMEOUT)
    admin_login.open("/administration")
    admin_login.form_exists_ad_correct()


@allure.severity(severity_level=Severity.NORMAL)
@allure.title("User registration page checking")
@allure.feature("Pages testing")
def test_user_registration(browser, base_url):
    user_reg_page = UserRegistrationPage(base_url, browser, TIMEOUT)
    user_reg_page.open("/?route=account/register")
    user_reg_page.form_exists()


@allure.severity(severity_level=Severity.CRITICAL)
@allure.title("Main page checking with failure")
@allure.feature("Pages testing")
def test_failed(browser, base_url):
    page = MainPage(base_url, browser, TIMEOUT)
    page.open('/')
    assert False