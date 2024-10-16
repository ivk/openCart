from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class AdminPage(BasePage):

    def open(self, url):
        self.browser.get(f"{self.base_url}{url}")
        element = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element(By.ID, "content"))
        assert "Please enter your login details." in element.text
        assert "Administration" in self.browser.title
        return element


    def form_exists_and_correct(self):
        assert self.browser.find_element(By.NAME, "username").is_enabled()
        assert self.browser.find_element(By.NAME, "password").is_enabled()
        btn = self.browser.find_element(By.TAG_NAME, "button")
        assert btn.text == "Login"
        assert btn.is_enabled()
        assert 'btn' in btn.get_attribute('class')

    def is_unauthorized(self, content):
        # logged out
        assert "Administration" in self.browser.title
        assert "Please enter your login details." in content.text

    def login(self, username, password):
        self.browser.find_element(By.NAME, "username").send_keys(username)
        self.browser.find_element(By.NAME, "password").send_keys(password)
        self.browser.find_element(By.TAG_NAME, 'button').click()

        el = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        assert 'Dashboard' == el.text
        assert 'John Doe' in self.browser.find_element(By.ID, 'nav-profile').text

    def logout(self):
        self.browser.find_element(By.CSS_SELECTOR, '#nav-logout a').click()
        self.wait.until(EC.url_changes('/administration/index.php?route=common/login'))
        assert "Administration" in self.browser.title
        assert self.browser.find_element(By.ID, 'form-login')