import pandas as pd
import streamlit as st
import os

# def quarter_to_date(quarter):
#         # Mapowanie kwartałów na miesiące
#         map_quarter_to_date = {
#         'Q1': '05',
#         'Q2': '08',
#         'Q3': '11',
#         'Q4': '02'
#         }
#         year, quarter = quarter.split('/')
#         month = map_quarter_to_date[quarter]
#         # Jeśli Q4, to miesiąc przypada na luty następnego roku
#         if quarter == 'Q4':
#             year = str(int(year) + 1)
#         return pd.to_datetime(f'{year}-{month}-01')

# @st.cache_data
# def prepare_price_data():
#     """
#     Prepares stock price data by reading CSV files from a specified directory,
#     renaming columns, converting date formats, and concatenating data into a single DataFrame.
#     """
#     directory = "Data/Daily_data"
#     df_price = pd.DataFrame(columns=['Data', 'Cena otwarcia', 'Cena najwyższa sessji', 'Cena najniższa sessji', 'Cena zamknięcia', 'Wolumen'])
#     stock_list = ['ACP', 'ALE', 'ALR', 'CCC', 'CDR', 'CPS', 'DNP', 'JSW', 'KGHM', 'LPP', 'LTS', 'MRC', 'OPL', 'PEO', 'PGE', 'PGN', 'PKN', 'PKO', 'PZU', 'SPL', 'TPE']
#     i = 0

#     for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)
#         if not filename[:3].upper() in stock_list:
#             continue
#         single_stock_data = pd.read_csv(file_path)
#     #     single_stock_data = single_stock_data.rename(columns={'Data': 'Date', 'Otwarcie': 'Open', 'Najwyzszy': 'Highest', 'Najnizszy': 'Lowest', 'Zamkniecie': 'Close', 'Wolumen': 'Volume'})
#         single_stock_data['Data'] = pd.to_datetime(single_stock_data.Data)
#         single_stock_data['Spółka'] = stock_list[i]
#         df_price = pd.concat([df_price, single_stock_data], ignore_index=True)
#         i += 1
#         print('Loaded file: ' + filename)

#     return df_price

@st.cache_data
def prepare_indicator_data():
    all_data = pd.read_csv('Data/app_all_data.csv')
    income_yearly = pd.read_csv('Data/app_income_yearly.csv')
    indicators = pd.read_csv('Data/app_indicators.csv')
    
    return all_data, income_yearly, indicators

# @st.cache_data
# def prepare_latest_indicator_data():
#     df_ind_latest = pd.read_csv('Data/Fundamental_indicators_latest.csv')
#     # Zamiana przecinków na kropki i rzutowanie kolumn numerycznych na liczby
#     num_cols = df_ind_latest.select_dtypes(include='object').columns
#     for col in num_cols:
#         df_ind_latest[col] = (
#             df_ind_latest[col]
#             .astype(str)
#             .str.replace(' ', '', regex=False)
#             .str.replace(',', '.', regex=False)
#         )
#         df_ind_latest[col] = pd.to_numeric(df_ind_latest[col], errors='ignore')
#     return df_ind_latest

# @st.cache_data
# def stock_latest_data():
#     """
#     Returns the latest stock data from the prepared price data.
#     """
#     df_price = prepare_price_data()
#     latest_data = df_price.groupby('Spółka').last().reset_index()
#     latest_data = latest_data.rename(columns={'Data': 'Ostatnia aktualizacja'})
#     return latest_data[['Spółka', 'Ostatnia aktualizacja']]