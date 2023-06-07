from scrapers.BBC import BBCScraper
from scrapers.daily_mail import DailyMailScraper
import scrapers.webscraper_utilities as webscraper_utilities
from scrapers.model.article import Article
import database.database_utilities as database
import time
import logging

logging.basicConfig(filename='main.log',
                    format= '%(asctime)s %(message)s',
                    
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

main_json = './json/main.json'
bbc_json = './json/bbc.json'
dailymail_json = './json/daily_mail.json'

def get_article_list(scraper) -> list[Article]:
    return scraper.get_front_page_articles()


bbc_scraper = BBCScraper()
daily_mail_scraper = DailyMailScraper()

webscraper_utilities.initialise_article_json(main_json)
webscraper_utilities.initialise_article_json(bbc_json)
webscraper_utilities.initialise_article_json(dailymail_json)

while True:

    logger.info('Starting data collection')

    bbc_list = get_article_list(bbc_scraper)
    daily_mail_list = get_article_list(daily_mail_scraper)

    logger.info('Writing results to JSON...')
    webscraper_utilities.write_article_list_to_json_file(bbc_list, main_json)
    webscraper_utilities.write_article_list_to_json_file(daily_mail_list, main_json)
    webscraper_utilities.extract_articles_by_site_and_write_to_json_file(main_json, bbc_json, 'BBC')
    webscraper_utilities.extract_articles_by_site_and_write_to_json_file(main_json, dailymail_json, 'Daily Mail')
    logger.info('Finished writing results to JSON')

    logger.info('Uploading articles to database...')
    my_database = database.connect_to_database()
    database.upsert_article_list(bbc_list, my_database)
    database.upsert_article_list(daily_mail_list, my_database)
    my_database.commit()
    my_database.close()
    logger.info("Successfully uploaded articles to database")

    logger.info('Data collection finished\n')

    time.sleep(3600)
