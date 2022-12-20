
import pandas as pd
from bs4 import BeautifulSoup
import requests
import openpyxl
import time
import datetime
import mysql.connector

#while True :
page = 1
name_list = []
project_list = []
location_list = []
price_list = []
while page <= 60 :
    url = 'https://lazudi.com/th/properties/condo-for-rent/%E0%B8%81%E0%B8%A3%E0%B8%B8%E0%B8%87%E0%B9%80%E0%B8%97%E0%B8%9E%E0%B8%A1%E0%B8%AB%E0%B8%B2%E0%B8%99%E0%B8%84%E0%B8%A3?propertyTypes=condo&page='+str(page)
    source = requests.get(url)
    source.encoding = "utf-8"
    soup = BeautifulSoup(source.text, 'html.parser')
    for c in soup.find_all('div',{'class':'search-details flex-grow-1'}):
        a = c.find('h2').text
        name_list.append(a)
        b = c.find('h3',{'class':'project-name'}).text
        project_list.append(b)
        d = c.find('h3',{'class':'location'}).text
        location_list.append(d)
        e = c.find('div',{'class':'group'}).text.replace(',','').replace('K','000').replace('฿ ','')
        price_list.append(e)
    print("Complete page : " , page)
    page += 1
df = pd.DataFrame([name_list,project_list,location_list,price_list]).transpose()
df.columns = ['Details','Project','Location','price']
#table.reset_index(inplace=True)
#df.replace('(^\s+|\s+$)', '', regex=True, inplace=True)
#with open('WebScraping\Condo_Scraped.json', 'w', encoding='utf-8') as file:
#    df.to_json(file, force_ascii=False, orient='records')
print("Complete round!!")

item_count = len(name_list)

con = mysql.connector.connect(
host = "localhost",
user = "root",
db = "mycondodb"
)
cursorpy = con.cursor()
for i in range(item_count) :
    date_now = datetime.datetime.now()
    query = "INSERT INTO condo_list (Details,Project,Location,Price) VALUES (%s , %s , %s ,%s)"
    value = (name_list[i],project_list[i],location_list[i],price_list[i])
    cursorpy.execute(query , value)

con.commit()
print(cursorpy)