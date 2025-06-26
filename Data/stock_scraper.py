from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

url = 'https://www.biznesradar.pl/gielda/akcje_gpw'
stock_data = []


response = requests.get(url)
soup = BeautifulSoup(response.text, features='html.parser')

stock_table = soup.find('table', attrs={"class": "table table--accent-header table--accent-first table--even table--nowrap table--sticky-first-col table--sticky-header"})

for stock in soup.find_all('tr', attrs={"class": "hot-row"}):
    full_name = stock.find('td').text
    if '(' not in full_name:
        ticker = full_name
        name = full_name
    else:
        ticker = full_name.split('(')[0].strip()
        name = full_name.split('(')[1].replace(')', '').strip()

    adress = 'https://www.biznesradar.pl' + stock.find('a').get("href")

    response_stock = requests.get(adress)
    print(adress)
    soup_stock = BeautifulSoup(response_stock.text, features='html.parser')
    stock_page = soup_stock.find('div', attrs={"class": "box-left"})
    stock_info = stock_page.find('table', attrs={"class": "profileSummary"})
    industry = None
    for tr in stock_info.find_all('tr'):
        th = tr.find('th')
        if th and 'Branża:' in th.text:
            td = tr.find('td')
            if td:
                a = td.find('a')
                if a:
                    industry = a.text.strip()
            break
    print(industry) 

    stock_data.append({'ticker': ticker, 'name': name, 'adress': adress, 'industry': industry})
    sleep(1)

stock_list = pd.DataFrame(stock_data)

stock_list.to_csv('Data/stock_list.csv', index=False)