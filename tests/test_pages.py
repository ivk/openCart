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

TIMEOUT = 1


def test_main(browser, base_url):
    browser.get(base_url)

    WebDriverWait(browser, timeout=TIMEOUT)

    assert "Your Store" in browser.title
    assert browser.find_element(By.ID, "logo").is_displayed()

    product_cards = browser.find_elements(By.CLASS_NAME, "product-thumb")
    assert len(product_cards) == 4

    assert browser.find_element(By.ID, "carousel-banner-1").is_displayed()
    assert "OpenCart" in browser.find_element(By.TAG_NAME, "footer").text


def test_catalogue(browser, base_url):
    browser.get(f"{base_url}/catalog/desktops")
    assert WebDriverWait(browser, TIMEOUT).until(lambda x: x.find_element(By.TAG_NAME, "main"))
    assert browser.find_element(By.ID, 'product-category').is_displayed()
    assert browser.find_element(By.CSS_SELECTOR, 'ul.breadcrumb').is_displayed()
    assert browser.find_element(By.CSS_SELECTOR, '#content h2').is_displayed()
    assert browser.find_element(By.ID, 'product-list').is_displayed()

    products = browser.find_elements(By.CLASS_NAME, 'product-thumb')
    assert len(products) > 4

    assert len(browser.find_elements(By.CSS_SELECTOR, 'ul.pagination li'))


def test_card(browser, base_url):
    browser.get(f"{base_url}/product/desktops/macbook")
    assert WebDriverWait(browser, TIMEOUT).until(lambda x: x.find_element(By.TAG_NAME, "main"))
    assert browser.find_element(By.CSS_SELECTOR, '#product-info #content').is_displayed()
    assert browser.find_element(By.TAG_NAME, 'h1').is_displayed()
    price = browser.find_element(By.CLASS_NAME, 'price-new').text
    assert '$' in price
    assert float(price[1:]) > 100



def test_admin_login_page(browser, base_url):
    browser.get(f"{base_url}/administration")

    element = WebDriverWait(browser, TIMEOUT).until(lambda x: x.find_element(By.ID, "content"))
    assert "Please enter your login details." in element.text

    assert "Administration" in browser.title
    assert browser.find_element(By.NAME, "username").is_enabled()
    assert browser.find_element(By.NAME, "password").is_enabled()

    btn = browser.find_element(By.TAG_NAME, "button")
    assert btn.text == "Login"
    assert btn.is_enabled()
    assert 'btn' in btn.get_attribute('class')


def test_user_registration(browser, base_url):
    browser.get(f"{base_url}/?route=account/register")
    assert WebDriverWait(browser, TIMEOUT).until(lambda x: x.find_element(By.TAG_NAME, "main"))
    assert browser.find_element(By.TAG_NAME, 'nav')
    assert browser.find_element(By.TAG_NAME, 'header').is_displayed()
    assert len(browser.find_elements(By.TAG_NAME, 'footer'))
    browser.find_element(By.CSS_SELECTOR, "main form")
    assert browser.find_element(By.CSS_SELECTOR, ".text-end button").is_enabled()


