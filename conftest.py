import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests (chrome/firefox)")
    parser.addoption("--base_url", action="store", default="https://www.python.org", help="Base URL for the tests")


@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--browser")

    if browser_name == "chrome":
        options = ChromeOptions()
        service = ChromeService()
        browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        # options.binary_location = '/home/irina/bin/'
        # service = FirefoxService(executable_path='/home/irina/bin/geckodriver')
        service = FirefoxService()
        browser = webdriver.Firefox(options=options, service=service)

    browser.maximize_window()

    yield browser

    browser.quit()


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base_url")

