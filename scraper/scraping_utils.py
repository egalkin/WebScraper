import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests.sessions import Session


def get_item_info(item: Tag) -> dict:
    response = dict()
    response['vacancy_name'] = item.find('div', {'class': 'search-item-name'}).find('a').text
    response['employer'] = item.find('div', {'class': 'vacancy-serp-item__meta-info'}).find('a').text
    response['location'] = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).text
    salary = item.find('div', {'class': 'vacancy-serp-item__sidebar'}).find('div')
    response['salary'] = 'з/п не указана' if salary is None else salary.text
    return response


def parse_html(data_list: list) -> list:
    variants_list = list()
    for data in data_list:
        items = data.find_all('div', {'class': 'vacancy-serp-item'})
        for item in items:
            variants_list.append(get_item_info(item))
    return variants_list


def contain_vacancy_list(data: str) -> Tag or None:
    soup = BeautifulSoup(data, features="lxml")
    item = soup.find('div', {'class': 'vacancy-serp-item'})
    result = soup.find('div', {'class': 'vacancy-serp'})
    if item is not None:
        return result
    return None


def load_page(page: int, session: Session, url_body: str) -> str:
    url = '{}&page={}'.format(url_body, page)
    r = session.get(url)
    return r.text


def get_pages(url: str) -> list:
    s = requests.session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'
    })
    page = 0
    page_list = list()
    while True:
        data = load_page(page, s, url)
        parsed_html = contain_vacancy_list(data)
        if parsed_html:
            page_list.append(parsed_html)
            page += 1
        else:
            break
    return page_list
