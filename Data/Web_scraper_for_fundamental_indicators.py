from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from time import sleep

stock_list_path = r"C:\Users\Kamil\OneDrive\Python projects\Stock-analysis\Data\stock_list.csv"

url_rachunek_zyskow_i_strat = 'https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/'
url_bilans = 'https://www.biznesradar.pl/raporty-finansowe-bilans/'
url_przeplywy_pieniezne = 'https://www.biznesradar.pl/raporty-finansowe-przeplywy-pieniezne/'
url_wartosc_rynkowa = 'https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/'
url_rentownosc = 'https://www.biznesradar.pl/wskazniki-rentownosci/'
url_przeplywy_pieniezne = 'https://www.biznesradar.pl/wskazniki-przeplywow-pienieznych/'
url_zadluzenie = 'https://www.biznesradar.pl/wskazniki-zadluzenia/'
url_plynnosc = 'https://www.biznesradar.pl/wskazniki-plynnosci/'
url_aktywnosc = 'https://www.biznesradar.pl/wskazniki-aktywnosci/'

market_val_list = []
income_list = []
profitability_list = []
cash_flow_list = []
liabilities_list = []
liquidity_list = []
activity_list = []

# get stock list from CSV
df_stock_list = pd.read_csv(stock_list_path)
stock_list = df_stock_list['ticker'].str.upper().tolist()

# function returns quarters from available data for a single stock
def get_quarters(soup):
    quarters = []
    for quarters_soup in soup.find_all('th', attrs={"class": "thq h"}):
        quarters.append(quarters_soup.text.split()[0])
    quarters.append(soup.find('th', attrs={"class": "thq h newest"}).text.split()[0])
    return quarters

def get_date(soup, indicator_tag):
    indicator_raw = soup.find('tr', attrs={"data-field": indicator_tag})
    indicators = []
    if indicator_raw:
        for indicator_soup in indicator_raw.find_all("td", attrs={"class": "h"}):
            if indicator_soup.find("span"):
                indicators.append(indicator_soup.find("span").text)
            else:
                indicators.append(None)
    else:
        indicators = [None for _ in range(len(get_quarters(soup)))]
    return indicators

def get_indicator(soup, indicator_tag):
    indicator_raw = soup.find('tr', attrs={"data-field": indicator_tag})
    indicators = []
    if indicator_raw:
        for indicator_soup in indicator_raw.find_all("td", attrs={"class": "h"}):
            if indicator_soup.find("span", attrs={"class": "pv"}):
                indicators.append(indicator_soup.find("span", attrs={"class": "pv"}).text)
            else:
                indicators.append(None)
    else:
        indicators = [None for _ in range(len(get_quarters(soup)))]
    return indicators

for index, row in df_stock_list.iterrows():
    stock = row['ticker']
    print('Loading data: ' + stock)

    # Financial reports
    # Income statement
    soup_rzis = BeautifulSoup(requests.get(url_rachunek_zyskow_i_strat + stock + ',Q').text, features='html.parser')
    if not soup_rzis.find('th', attrs={"class": "thq h newest"}):
        print(f'No data found for {stock}, skipping...')
        continue
    
    income_quarters = get_quarters(soup_rzis)
    income = pd.DataFrame(list(zip(income_quarters)), columns=['Kwartały'])
    income.insert(0, 'Ticker', stock)
    income.insert(0, 'Nazwa', row['name'])
    income['Data'] = get_date(soup_rzis, 'PrimaryReport')
    income['Przychody ze sprzedaży'] = get_indicator(soup_rzis, 'IncomeRevenues')
    income['Zysk ze sprzedaży'] = get_indicator(soup_rzis, 'IncomeGrossProfit')
    income['Zysk operacyjny (EBIT)'] = get_indicator(soup_rzis, 'IncomeEBIT')
    income['Zysk z działalności gospodarczej	'] = get_indicator(soup_rzis, 'IncomeNetGrossProfit')
    income['Zysk przed opodatkowaniem'] = get_indicator(soup_rzis, 'IncomeBeforeTaxProfit')
    income['Zysk netto'] = get_indicator(soup_rzis, 'IncomeNetProfit')
    income['EBITDA'] = get_indicator(soup_rzis, 'IncomeEBITDA')

    income_list.append(income)

    # Market value indicators
    soup_wr = BeautifulSoup(requests.get(url_wartosc_rynkowa + stock).text, features='html.parser')
    if not soup_wr.find('th', attrs={"class": "thq h newest"}):
        print(f'No data found for {stock}, skipping...')
        continue
    stock_quarters = get_quarters(soup_wr)
    Kurs = get_indicator(soup_wr, 'Quote')
    WK = get_indicator(soup_wr, 'WK')
    C_WK = get_indicator(soup_wr, 'CWK')
    Z = get_indicator(soup_wr, 'Z')
    C_Z = get_indicator(soup_wr, 'CZ')
    P = get_indicator(soup_wr, 'P')
    C_P = get_indicator(soup_wr, 'CP')
    ZO = get_indicator(soup_wr, 'ZO')
    C_ZO = get_indicator(soup_wr, 'CZO')
    WK_Graham = get_indicator(soup_wr, 'WKGraham')
    C_WK_Graham = get_indicator(soup_wr, 'CWKGraham')
    EV = get_indicator(soup_wr, 'EV')
    EV_P = get_indicator(soup_wr, 'EVP')
    EV_EBIT = get_indicator(soup_wr, 'EVEBIT')
    EV_EBITDA = get_indicator(soup_wr, 'EVEBITDA')

    market_val = pd.DataFrame(list(zip(stock_quarters, Kurs, WK, C_WK, Z, C_Z, P, C_P, ZO, C_ZO, WK_Graham, C_WK_Graham, EV, EV_P, EV_EBITDA, EV_EBIT)),
                              columns=['Kwartały', 'Kurs', 'Wartość księgowa', 'Cena/WK', 'Zysk na akcję', 'Cena/Zysk',
                                       'Przychód', 'Cena/Przychód', 'Zysk operacyjny', 'Cena/Zysk operacyjny',
                                       'Wartość księgowa Grahama', 'Cena/Wartość księgowa Grahama',
                                       'Wartość przedsiębiorstwa', 'Wartość przedsiębiorstwa/Przychody',
                                       'Wartość przedsiębiorstwa/EBITDA', 'Wartość przedsiębiorstwa/EBIT'])
    market_val.insert(0, 'Ticker', stock)
    market_val.insert(0, 'Nazwa', row['name'])

    market_val_list.append(market_val)
    

    # Profitability indicators
    soup_rentownosc = BeautifulSoup(requests.get(url_rentownosc + stock).text, features='html.parser')
    profitability = market_val.copy().loc[:, ['Ticker', 'Nazwa', 'Kwartały']]
    profitability['ROE'] = get_indicator(soup_rentownosc, 'ROE')
    profitability['ROA'] = get_indicator(soup_rentownosc, 'ROA')
    profitability['Marża zysku operacyjnego'] = get_indicator(soup_rentownosc, 'OPM')
    profitability['Marża zysku netto'] = get_indicator(soup_rentownosc, 'ROS')
    profitability['Marża zysku ze sprzedaży'] = get_indicator(soup_rentownosc, 'RS')
    profitability['Marża zysku brutto'] = get_indicator(soup_rentownosc, 'GPM')
    profitability['Marża zysku brutto ze sprzedaży'] = get_indicator(soup_rentownosc, 'RBS')
    profitability['Rentowność operacyjna aktywów'] = get_indicator(soup_rentownosc, 'ROPA')
    profitability_list.append(profitability)

    # Cash flow indicators
    soup_pp = BeautifulSoup(requests.get(url_przeplywy_pieniezne + stock).text, features='html.parser')
    cash_flow = market_val.copy().loc[:, ['Ticker', 'Nazwa', 'Kwartały']]
    cash_flow['Udział zysku netto w przepływach operacyjnych'] = get_indicator(soup_pp, 'ZNPO')
    cash_flow['Wskaźnik źródeł finansowania inwestycji'] = get_indicator(soup_pp, 'ZFI')
    cash_flow_list.append(cash_flow)

    # Liabilities indicators
    soup_zadluzenie = BeautifulSoup(requests.get(url_zadluzenie + stock).text, features='html.parser')
    liabilities = market_val.copy().loc[:, ['Ticker', 'Nazwa', 'Kwartały']]
    liabilities['Zadłużenie ogólne'] = get_indicator(soup_zadluzenie, 'DTAR')
    liabilities['Zadłużenie kapitału własnego'] = get_indicator(soup_zadluzenie, 'CG')
    liabilities['Zadłużenie długoterminowe'] = get_indicator(soup_zadluzenie, 'LDER')
    liabilities['Zadłużenie środków trwałych'] = get_indicator(soup_zadluzenie, 'PZAT')
    liabilities['Pokrycie aktywów trwałych kapitałami stałymi'] = get_indicator(soup_zadluzenie, 'PELDR')
    liabilities['Trwałość struktury finansowania'] = get_indicator(soup_zadluzenie, 'TSF')
    liabilities['Zastosowanie kapitału obcego'] = get_indicator(soup_zadluzenie, 'ZKO')
    liabilities['Wskaźnik ogólnej sytuacji finansowej'] = get_indicator(soup_zadluzenie, 'OSF')
    liabilities['Zadłużenie netto'] = get_indicator(soup_zadluzenie, 'NetDebt')
    liabilities['Zadłużenie netto / EBITDA'] = get_indicator(soup_zadluzenie, 'NetDebtEBITDA')
    liabilities['Zadłużenie finansowe netto'] = get_indicator(soup_zadluzenie, 'DebtFin')
    liabilities['Zadłużenie finansowe netto / EBITDA'] = get_indicator(soup_zadluzenie, 'DebtFinEBITDA')
    liabilities_list.append(liabilities)

    # Liquidity indicators
    soup_plynnosc = BeautifulSoup(requests.get(url_plynnosc + stock).text, features='html.parser')
    liquidity = market_val.copy().loc[:, ['Ticker', 'Nazwa', 'Kwartały']]
    liquidity['I stopień pokrycia'] = get_indicator(soup_plynnosc, 'SP1')
    liquidity['II stopień pokrycia'] = get_indicator(soup_plynnosc, 'SP2')
    liquidity['Płynność gotówkowa'] = get_indicator(soup_plynnosc, 'CAR')
    liquidity['Płynność szybka'] = get_indicator(soup_plynnosc, 'QR')
    liquidity['Płynność bieżąca'] = get_indicator(soup_plynnosc, 'CR')
    liquidity['Płynność podwyższona'] = get_indicator(soup_plynnosc, 'PP')
    liquidity['Pokrycie zobowiązań należnościami'] = get_indicator(soup_plynnosc, 'RCLR')
    liquidity['Udział kapitału pracującego w aktywach'] = get_indicator(soup_plynnosc, 'KP')
    liquidity_list.append(liquidity)

    # Activity indicators
    soup_aktywnosc = BeautifulSoup(requests.get(url_aktywnosc + stock).text, features='html.parser')
    activity = market_val.copy().loc[:, ['Ticker', 'Nazwa', 'Kwartały']]
    activity['Pokrycie kosztów kapitałem obrotowym'] = get_indicator(soup_aktywnosc, 'PKKO')
    activity['Rotacja należności'] = get_indicator(soup_aktywnosc, 'RN')
    activity['Cykl należności'] = get_indicator(soup_aktywnosc, 'CRN')
    activity['Cykl zobowiązań'] = get_indicator(soup_aktywnosc, 'CPZ')
    activity['Rotacja zapasów'] = get_indicator(soup_aktywnosc, 'RZ')
    activity['Cykl zapasów'] = get_indicator(soup_aktywnosc, 'CRZ')
    activity['Rotacja majątku obrotowego'] = get_indicator(soup_aktywnosc, 'RMO')
    activity['Rotacja majątku trwałego'] = get_indicator(soup_aktywnosc, 'RMT')
    activity['Rotacja majątku ogółem'] = get_indicator(soup_aktywnosc, 'RM')
    activity['Cykl operacyjny'] = get_indicator(soup_aktywnosc, 'COP')
    activity['Cykl konwersji gotówki'] = get_indicator(soup_aktywnosc, 'CSP')
    activity_list.append(activity)
    sleep(2)  # to avoid overwhelming the site


pd.concat(income_list).to_csv('income', index=False)
pd.concat(market_val_list).to_csv('market_value', index=False)
pd.concat(profitability_list).to_csv('profitability', index=False)
pd.concat(cash_flow_list).to_csv('cash_flow', index=False)
pd.concat(liabilities_list).to_csv('liabilities', index=False)
pd.concat(liquidity_list).to_csv('liquidity', index=False)
pd.concat(activity_list).to_csv('activity', index=False)
print('Files created')
