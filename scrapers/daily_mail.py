from scrapers.model.article import Article
import requests
from bs4 import BeautifulSoup
import re
import logging


class DailyMailScraper:
    def __init__(self):
        self.logger = logging.getLogger('main.log')
        self.base_url = "https://www.dailymail.co.uk"
        self.url = self.base_url + "/home/index.html"
        self.banned_titles = ['Contributors', 
                              'About MailOnline',
                              'MORE INFO',
                              'click here',
                              ]

    def get_front_page_articles(self) -> list[Article]:

        r1 = requests.get(self.url)
        frontpage = r1.content
        soup = BeautifulSoup(frontpage, "html.parser")
        articles = soup.find_all('a')

        articles_titles_and_links = []

        for article in articles:
            if 'href' in article.attrs and 'article' in article.attrs['href']:
                article_title = article.get_text()
                article_title = article_title.strip()
                article_title = article_title.replace('\n', '')

                if article_title not in self.banned_titles:
                    match = re.sub(r'(\d+(?:\.\d+)?k? )?(comments|comment|videos|video)', '', article_title)

                    if match != '':
                        if [article.get_text(), article.attrs['href']] not in articles_titles_and_links:
                            articles_titles_and_links.append([article_title, article.attrs['href']])
                    
        return_list = []

        for title_link in articles_titles_and_links:
                return_list.append(Article(title_link[0], "Daily Mail", self.base_url + title_link[1]))

        self.logger.info('    - Daily Mail has ' + str(len(return_list)) + ' articles on its front page')

        return return_list