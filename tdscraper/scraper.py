import re
import urllib.request

from bs4 import BeautifulSoup
from datetime import datetime


URL = "https://taxas-tesouro.com"


def get_html_from_url(url: str) -> str:
    """Get the html content from an url."""
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html.decode()


def extract_body_content(html: str) -> str:
    """Clean and keep only the body content."""
    body_start = html.index("<body")
    body_end = html.index("</body>")
    return html[body_start:body_end+7]


def create_beautiful_soup_from_html(html: str) -> BeautifulSoup:
    """Create a BeautifulSoup instance from a html."""
    return BeautifulSoup(html, "html.parser")


def get_last_content_update_date(bs: BeautifulSoup) -> datetime:
    """Extract the last update date from BeautifulSoup structure."""
    last_update_tag = bs.find("main").find(
        "span", attrs={"class": "text-xs text-gray-600"}
    )
    res = re.search(r"\d{1,2}/\d{1,2}/\d{2,4} \d{1,2}:\d{1,2}", last_update_tag.text)

    return datetime.strptime(res.group(), "%d/%m/%Y %H:%M")


def get_titles_to_invest_data(bs: BeautifulSoup) -> list:
    """Get the information of titles available to invest."""
    titles_tags = bs.find_all('a', href=re.compile(r"investir"))
    titles = []
    for tag in titles_tags:
        name = tag.find("span", property="name").text
        price = tag.find("span", property="price").text
        interest_rate = tag.find("span", property="interestRate").text
        titles.append({
            "name": name,
            "price": float(price.split()[1].replace('.', '').replace(',', '.')),
            "interest_rate": float(interest_rate.replace('%', ''))
        })
    return titles


def get_titles_to_redeem_data(bs: BeautifulSoup) -> list:
    """Get the information of titles available to redeem."""
    titles_tags = bs.find_all('a', href=re.compile(r"resgatar"))
    titles = []
    for tag in titles_tags:
        name = tag.find("span", property="name").text
        price = tag.find(
            "div",
            attrs={"class": "hidden sm:block flex-1 ml-2 text-right text-gray-700"}
        ).text
        interest_rate = tag.find(
            "div",
            attrs={"class": "flex-1 ml-2 text-right"}
        ).text
        titles.append({
            "name": name,
            "price": float(price.split()[1].replace('.', '').replace(',', '.')),
            "interest_rate": float(interest_rate.replace('%', ''))
        })
    return titles


def get_titles_full_list(bs: BeautifulSoup) -> dict:
    """Get a list with all available titles."""
    invest = get_titles_to_invest_data(bs)
    redeem = get_titles_to_redeem_data(bs)
    return {'invest': invest, 'redeem': redeem}
