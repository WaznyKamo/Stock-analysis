import pandas as pd
import streamlit as st
import os
import numpy as np


@st.cache_data
def prepare_indicator_data():
    all_data = pd.read_csv('Data/Quarterly_data/app_all_data.csv')
    income_yearly = pd.read_csv('Data/Quarterly_data/app_income_yearly.csv')
    indicators = pd.read_csv('Data/Quarterly_data/app_indicators.csv')
    financial_report = pd.read_csv('Data/Yearly_data/financial_report.csv')
    
    return all_data, income_yearly, indicators, financial_report

@st.cache_data
def calculate_cagr(financial_report, window):
    cols_to_analyze = [col for col in financial_report.columns if col not in ['Spółka', 'Rok', 'Lata raportu']]
    results = []

    for company, group in financial_report.groupby('Spółka'):
        row = {'Spółka': company}
        for col in cols_to_analyze:
            try:
                if window == "Brak":
                    # Najnowszy rekord (Lata raportu == 0), najstarszy rekord (Lata raportu == max)
                    val_0 = group.loc[group['Lata raportu'] == 0, col].values[0]
                    val_w = group.loc[group['Lata raportu'] == group['Lata raportu'].max(), col].values[0]
                    n = group['Lata raportu'].max()
                else:
                    val_0 = group.loc[group['Lata raportu'] == 0, col].values[0]
                    val_w = group.loc[group['Lata raportu'] == window, col].values[0]
                    n = window
                if pd.notnull(val_0) and pd.notnull(val_w) and val_w != 0 and (val_0 / val_w) > 0:
                    row[col] = round(((val_0 / val_w) ** (1/n) - 1) * 100, 2)
                else:
                    row[col] = np.nan
            except IndexError:
                row[col] = np.nan
        results.append(row)

    df_window_ratio = pd.DataFrame(results)
    return df_window_ratio

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