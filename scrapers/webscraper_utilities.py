from scrapers.model.article import Article
import json
import datetime


def write_single_article_to_json_file(article: Article, file_name: str):
    with open(file_name, 'r+') as json_file:
        json_data = json.load(json_file)
        json_data['article_list'].append(article.to_json())
        json_file.seek(0)
        json.dump(json_data, json_file)

def initialise_article_json(file_name: str):
    try:
        new_file = open(file_name, 'x')
        new_file.write('{"article_list": []}')
        new_file.close()
    except FileExistsError:
        pass

def write_article_list_to_json_file(article_list: list[Article], file_name: str):

    article_list_json = []
    for article in article_list:
        article_list_json.append(article.to_json())

    with open(file_name, 'r+') as json_file:
        json_data = json.load(json_file)
        for article_json in article_list_json:
            add_article_to_json_data(article_json, json_data)
        json_file.seek(0)
        json.dump(json_data, json_file)

def add_article_to_json_data(article_json, json_data):

    json_data_articles = json_data['article_list']

    for i in range(len(json_data_articles)):
        if article_json['title'] == json_data_articles[i]['title']:
            json_data_articles[i]['last_seen_at'] = str(datetime.datetime.now())[:-7]
            return json_data
        
    json_data['article_list'].append(article_json)

    return json_data

def extract_articles_by_site_and_write_to_json_file(json_read_file_name: str, json_write_file_name: str, site: str):
    with open(json_read_file_name, 'r') as json_read_file:
        json_data = json.load(json_read_file)
        articles_json_by_site = []
        for article_json in json_data['article_list']:
            if article_json['site'] == site:
                articles_json_by_site.append(article_json)

    with open(json_write_file_name, 'r+') as json_write_file:
        json_data = json.load(json_write_file)
        json_data['article_list'] = articles_json_by_site
        json_write_file.seek(0)
        json.dump(json_data, json_write_file)

    
    
