from getopt import getopt
from venv import logger

import allure
import pytest
import logging
import datetime
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
    parser.addoption("--log_level", action="store", default="INFO")


# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, "rep_" + rep.when, rep)
#     return rep


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    log_level = request.config.getoption("--log_level")

    test_name = request.node.originalname
    logger = logging.getLogger(test_name)
    file_handler = logging.FileHandler(f"logs/{test_name}.log")
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info("===> Test %s started at %s" % (request.node.name, datetime.datetime.now()))

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

    browser.log_level = log_level
    browser.logger = logger
    browser.test_name = test_name

    logger.info("Browser %s started" % browser_name)

    browser.maximize_window()

    yield browser

    browser.quit()
    logger.info("===> Test %s finished at %s" % (request.node.name, datetime.datetime.now()))


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base_url")


def pytest_exception_interact(node, call, report):
    if report.failed:
        print('test failed')
        logger = logging.getLogger(node.name)
        logger.info(f"ERROR Test {node.name} failed!!!")
        driver = node.funcargs['browser']
        allure.attach(
                        driver.get_screenshot_as_png(),
                        name="screenshot_on_failure",
                        attachment_type=allure.attachment_type.PNG
                    )


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, "rep_" + rep.when, rep)
#     if rep.when == "call" and rep.failed:
#         try:
#             driver = item.funcargs['browser']
#             allure.attach(
#                 driver.get_screenshot_as_png(),
#                 name="screenshot_on_failure",
#                 attachment_type=allure.attachment_type.PNG
#             )
#         except Exception as e:
#             logging.error(f"Failed to take screenshot: {e}")