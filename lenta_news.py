from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['lesson4lenta']
lenta_news_collection = db.lenta_news


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

url = 'https://lenta.ru/'
session = requests.Session()
response = session.get(url, headers=header)
dom = html.fromstring(response.text)

main_news = []
items = dom.xpath("//div[contains(@class,'topnews')]")
pprint(items)
for item in items:
    news = {}
    name_of_resource = "lenta.ru"
    name = item.xpath(".//h3[@class='card-big__title']//text()" 
                      "|" 
                      ".//span[@class='card-mini__title']//text()")
    link = item.xpath(".//a[@class='card-big _topnews _news']//@href"
                      "|"
                      ".//a[@class='card-mini _topnews']//@href")
    publication_date = item.xpath(".//time[@class='card-mini__date']//text()")

    news['name_of_resource'] = name_of_resource
    news['name'] = name
    news['link'] = link
    news['publication_date'] = publication_date

##Задание 2 Сложить собранные новости в БД
    try:
        lenta_news_collection.insert_one(news)
    except errors.DuplicateKeyError:
        print(f"Document with name = {main_news['name']} is already exists")


for item in lenta_news_collection.find({}):
   pprint(item)
