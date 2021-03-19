import pytest
from bs4 import BeautifulSoup
from datetime import datetime
from tdscraper import scraper


@pytest.fixture
def mock_get_html_from_url(monkeypatch):
    """To avoid many requests to the scrapped site this mock read the
        date from a file.
        """
    def mock_html_content(*args, **kwargs):
        with open('tests/tdscraper/taxas-tesouro.html', 'r') as f:
            return ''.join(f.readlines())
    monkeypatch.setattr(scraper, "get_html_from_url", mock_html_content)


def test_get_html_from_url(mock_get_html_from_url):
    html = scraper.get_html_from_url("")
    assert '<html' in html
    assert '</html>' in html
    assert '<body' in html
    assert '</body>' in html


def test_extract_body_content(mock_get_html_from_url):
    html = scraper.get_html_from_url("")
    body = scraper.extract_body_content(html)
    assert body.startswith('<body>')
    assert body.endswith('</body>')


def test_load_beautiful_soup_from_html(mock_get_html_from_url):
    html = scraper.get_html_from_url("")
    bs = scraper.create_beautiful_soup_from_html(html)
    assert isinstance(bs, BeautifulSoup)


def test_get_last_content_update_date(mock_get_html_from_url):
    raw_data = scraper.get_html_from_url("")
    html = scraper.extract_body_content(raw_data)
    bs = scraper.create_beautiful_soup_from_html(html)
    last_update = scraper.get_last_content_update_date(bs)
    assert isinstance(last_update, datetime)


def test_get_titles_to_invest_data(mock_get_html_from_url):
    raw_data = scraper.get_html_from_url("")
    html = scraper.extract_body_content(raw_data)
    bs = scraper.create_beautiful_soup_from_html(html)
    data = scraper.get_titles_to_invest_data(bs)
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert ['name', 'price', 'interest_rate'] == list(data[0].keys())


def test_get_titles_to_redeem_data(mock_get_html_from_url):
    raw_data = scraper.get_html_from_url("")
    html = scraper.extract_body_content(raw_data)
    bs = scraper.create_beautiful_soup_from_html(html)
    data = scraper.get_titles_to_redeem_data(bs)
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert ['name', 'price', 'interest_rate'] == list(data[0].keys())


def test_get_titles_full_list(mock_get_html_from_url):
    raw_data = scraper.get_html_from_url("")
    html = scraper.extract_body_content(raw_data)
    bs = scraper.create_beautiful_soup_from_html(html)
    all_titles = scraper.get_titles_full_list(bs)
    assert isinstance(all_titles, dict)
    assert len(all_titles['invest']) > 0
    assert len(all_titles['redeem']) > 0
