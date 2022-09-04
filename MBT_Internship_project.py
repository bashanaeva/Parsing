from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from pymongo import MongoClient
from pymongo import errors
import pprint


client = MongoClient('127.0.0.1', 27017)
db = client['MBT_Internship(1)']
MBT_Internship_collection = db.MBT_Internship_collection


s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)
driver.get('http://portfolio.dgu.ru/ratingviewer.aspx')


department = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$FilList')
select_d = Select(department)
select_d.select_by_value('1')
department.submit()
time.sleep(1)

try:
    faculty = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$FacList')
    select_f = Select(faculty)
    select_f.select_by_value('20')
    faculty.submit()
except:
   time.sleep(1)

try:
    spesiality = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$DeptList')
    select_s = Select(spesiality)
    select_s.select_by_value('2003')
    spesiality.submit()
except:
    time.sleep(1)

try:
    kind = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$EdukindList')
    select_k = Select(kind)
    select_k.select_by_value('1')
    kind.submit()
except:
    time.sleep(1)

try:
   course = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$CourseList')
   select_c = Select(course)
   select_c.select_by_value('3')
   course.submit()
except:
   time.sleep(1)

try:
   year = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$SYearList')
   select_y = Select(year)
   select_y.select_by_value('2021')
   year.submit()
except:
   time.sleep(1)

try:
    group = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$GroupList')
    select_g = Select(year)
    select_g.select_by_value('ИСиТ')
    group.submit()
except:
    time.sleep(1)

try:
    session = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$SessList')
    select_session = Select(session)
    select_session.select_by_value('летний')
    session.submit()
except:
    time.sleep(1)

try:
    category = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$RaitCategoryDDL')
    select_category = Select(category)
    select_category.select_by_value('Итог')
    category.submit()
except:
    time.sleep(1)

button = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$GoBtn')
button.click()
time.sleep(1)


# items = driver.find_elements(By.XPATH,'.//table[@class="table"]')
# for item in items:
     ### Row_Nummber = item.find_elements(By.XPATH,'.//tr[@style="background-color:#F3F3F3;"]  | //tr[@style="background-color:White;"] | //td[contains(text(),"Место")]')
FIO = driver.find_elements(By.XPATH,'.//tr[@style="background-color:#F3F3F3;"]  | //tr[@style="background-color:White;"] | /a[@onclick=" "]/text()')
for i in FIO:
     total_info = ({'all_info':i.text})
     print(total_info)

     try:
         MBT_Internship_collection.insert_one(total_info)
     except errors.DuplicateKeyError:
         print(f"Document with name = {total_info['all_info']} is already exists")


driver.close()

