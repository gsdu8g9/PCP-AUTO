from db.data_provider import DataProvider
import random
import requests
from bs4 import BeautifulSoup
import re


HEADERS = (
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)'
)

URL_PATTERN = 'http://anekdotov.net/anekdot/random{}.html'

# Сколько страниц парсить
COUNTER = 20


def parse():
    db = DataProvider()

    for i in range(0, COUNTER):
        user_agent = {
            'User-Agent': HEADERS[random.randint(0, len(HEADERS) - 1)]
        }

        current_url = URL_PATTERN.format(i + 1)

        # Получаем исходник страницы
        r = requests.get(current_url, headers=user_agent)
        r.encoding = 'Windows-1251'
        page_html = r.text

        soup = BeautifulSoup(page_html, 'html.parser')
        jokes_on_page = soup.find_all(attrs={'align': 'justify'})

        for joke_html in jokes_on_page:
            # Заменяем <br> на \n
            html_format = str(joke_html).replace('<br>', '\n')

            # Экранируем кавычки для sqlite
            html_format = html_format.replace('"', '""').replace("'", "''")

            html_format = html_format.replace('анекдотов.net', '')

            # Убираем лишние html-теги
            joke_text = re.sub(r'\<[^>]*\>', '', html_format)

            if len(joke_text) >= 550:
                db.add_new_text(joke_text)

    db.close_conn()