from scrapers.model.article import Article
import requests
from bs4 import BeautifulSoup
import logging


class BBCScraper:
    def __init__(self):
        self.logger = logging.getLogger('main.log')
        self.base_url = "https://www.bbc.co.uk"
        self.url = self.base_url + "/news"

    def get_front_page_articles(self) -> list[Article]:

        banned_titles = ['Family & Education',
                         'Isle of Man',
                         'US & Canada',
                         'Technology of Business',
                         'Family & Education Home',
                         'Entertainment & Arts',
                         'Highlands & Islands',
                         'Cost of Living',
                         'War in Ukraine']

        r1 = requests.get(self.url)
        frontpage = r1.content
        soup = BeautifulSoup(frontpage, "html.parser")
        articles = soup.find_all('a')
        articles_titles_and_links = []

        for article in articles:
            if not any(substring in article.get_text() for substring in banned_titles):
                if len(article.attrs['href']) > 0 and article.attrs['href'][0] == '/':
                    if len(article.get_text().split()) > 2:
                        if [article.get_text(), article.attrs['href']] not in articles_titles_and_links:
                            articles_titles_and_links.append([article.get_text(), article.attrs['href']])

        return_list = []

        for title_link in articles_titles_and_links:
            if title_link[0] not in ['', 'BBC Radio 5 Live', 'BBC News']:
                if title_link[0][:5] == 'Video':
                    title_link[0] = title_link[0][5:]
                return_list.append(Article(title_link[0], "BBC", self.base_url + title_link[1]))

        self.logger.info('    - BBC has ' + str(len(return_list)) + ' articles on its front page')

        return return_list