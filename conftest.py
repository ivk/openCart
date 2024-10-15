from random import choices

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

TIMEOUT = 1


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests (chrome/firefox)", choices=('chrome', 'firefox'))
    parser.addoption("--headless", action="store", default="false", help="Use headless browser (false/true)", choices=('true', 'false'))
    parser.addoption("--base_url", action="store", default="http://192.168.10.79:8081/", help="Base URL for the tests")


@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless == 'true':
            options.add_argument("-headless")
            options.add_argument('window-size=1920,1080')
        service = ChromeService()
        browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless == 'true':
            # for the god sake, don't use it ever! tests become smelly
            options.add_argument("-headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
        service = FirefoxService()
        browser = webdriver.Firefox(options=options, service=service)

    browser.maximize_window()

    yield browser

    browser.quit()


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base_url")

