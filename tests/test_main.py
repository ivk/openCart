def test_page_title(browser, base_url):
    browser.get(base_url)
    assert "Python" in browser.title


def test_search_functionality(browser, base_url):
    browser.get(base_url)
    search_input = browser.find_element("name", "q")
    search_input.send_keys("pytest")
    search_input.submit()
    assert "Python.org" in browser.title
    assert "pytest" in browser.page_source
