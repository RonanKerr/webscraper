import psycopg2
import datetime
import time
from scrapers.model.article import Article
import logging

upsert_article_sql = "INSERT INTO media.sites(title, site, link, creation_time, last_seen_at) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (title) DO UPDATE SET last_seen_at = %s"


def upsert_article(article: Article, connection):

    my_cursor = connection.cursor()
    
    my_cursor.execute(upsert_article_sql, (article.title, 
                                          article.site, 
                                          article.link, 
                                          str(article.creation_time),
                                          str(article.last_seen_at),
                                          str(article.last_seen_at)))
    my_cursor.close()

def upsert_article_list(article_list: list[Article], connection):

    for article in article_list:
        upsert_article(article, connection)


def connect_to_database():
    logger = logging.getLogger('main.log')
    try:
        my_connection = psycopg2.connect(database = 'get_you_own_bloody_database',
                            user ='get_you_own_bloody_database',
                            password = 'get_you_own_bloody_database',
                            host = 'rget_you_own_bloody_database',
                            port = 'get_you_own_bloody_database'
                            )
    except Exception as e:
        logger.exception(e)
        logger.warning('\n attempting to reconnect in five minutes... \n')
        time.sleep(300)
        connect_to_database()





    return my_connection




def run_test_sql():
    my_connection = connect_to_database()

    article = Article('this one trick will make your doctor hate you', 'test', 'example.com', datetime.datetime.now(), datetime.datetime.now())

    upsert_article(article, my_connection)

    my_connection.commit()
    my_connection.close()
