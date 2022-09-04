from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
from pprint import pprint
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_db22']
mvideo_collection = db.mvideo_collection


# Вариант II
# 2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
options = Options()
options.add_argument("start-maximized")
s = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)
driver.get("https://www.mvideo.ru/")
time.sleep(2)


scrolling_position = 0
while True:
    try:
        ## button_in_trend = driver.find_element(By.XPATH, '//*[.=" В тренде "]') ##нашел 1 элемент через chroPath,а здесь не нашел.
        button_in_trend = driver.find_element(By.XPATH, ".//span[contains(text(),' В тренде ')]/../..")
        button_in_trend.click()
        scrolling_position += 300
        driver.execute_script(f"window.scrollTo(0, {scrolling_position})")
        time.sleep(1)
        break
    except NoSuchElementException:
        scrolling_position += 100
        driver.execute_script(f"window.scrollTo(0, {scrolling_position})")
        time.sleep(1)


items_in_trends = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[@class='title']")
for item in items_in_trends:
    name = item.text
    href = item.find_element(By.XPATH, "./a").get_attribute('href')
    # price = item.find_element(By.XPATH, ".//span[@class='price__main-value']").text
    # stars = item.find_elements(By.XPATH, ".//span[@class='value ng-star-inserted']//text()")
    # bonus = item.find_elements(By.XPATH, ".//span[@class='mbonus-block__value']//text()")
    #
    # print(price)


    trends_search = len(list(mvideo_collection.find({'refference': href})))
    if trends_search == 0:
        articles = {
            'name': name,
            'href': href,
            # 'price': price,
            'in_group': 'IN TRENDS',
            'resourse': 'https://www.mvideo.ru/',
            # 'bonus_you_get': bonus
        }
        mvideo_collection.insert_one(articles)

driver.close()