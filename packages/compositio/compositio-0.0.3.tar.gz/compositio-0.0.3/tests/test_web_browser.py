import pytest
from blne.web_browser import WebBrowser

def test_web_browser_success(requests_mock):
    url = "http://example.com"
    content = "<html>Example</html>"
    requests_mock.get(url, text=content)
    
    browser = WebBrowser()
    result = browser.browse(url)
    
    assert result == content

def test_web_browser_failure(requests_mock):
    url = "http://example.com"
    requests_mock.get(url, status_code=404)
    
    browser = WebBrowser()
    result = browser.browse(url)
    
    assert result is None
