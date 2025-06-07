import pandas as pd

read_csv_path = r"C:\Users\Kamil\OneDrive\Python projects\Stock-analysis\Data\Fundamental_indicators.csv"
write_csv_path = r"C:\Users\Kamil\OneDrive\Python projects\Stock-analysis\Data\Fundamental_indicators_latest.csv"

df_ind = pd.read_csv(read_csv_path)

def quarter_to_date(quarter):
        # Mapowanie kwartałów na miesiące
        map_quarter_to_date = {
        'Q1': '05',
        'Q2': '08',
        'Q3': '11',
        'Q4': '02'
        }
        year, quarter = quarter.split('/')
        month = map_quarter_to_date[quarter]
        # Jeśli Q4, to miesiąc przypada na luty następnego roku
        if quarter == 'Q4':
            year = str(int(year) + 1)
        return pd.to_datetime(f'{year}-{month}-01')

df_ind['Data'] = df_ind['Kwartały'].apply(quarter_to_date)

df_latest = df_ind.loc[df_ind.groupby('Spółka')['Data'].idxmax()].reset_index(drop=True)

# print(df_latest.head())

df_latest.to_csv(write_csv_path, index=False)