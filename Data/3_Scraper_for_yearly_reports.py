import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

stock_list = r"C:\Users\Kamil\OneDrive\Python projects\Stock-analysis\Data\stock_list.csv"

BASE_URL = "https://www.biznesradar.pl/{}"
SECTIONS = {
    "zysk": "raporty-finansowe-rachunek-zyskow-i-strat/{}",
    "bilans": "raporty-finansowe-bilans/{}",
    "przeplywy": "raporty-finansowe-przeplywy-pieniezne/{}",
}

OUTPUT_FILES = {
    "zysk": "zysk.csv",
    "bilans": "bilans.csv",
    "przeplywy": "przeplywy.csv",
}

def parse_number(text):
    try:
        text = text.replace('\xa0', '').replace(' ', '').replace(',', '.')
        if text == '':
            return None
        return float(text)
    except ValueError:
        return None

def get_first_text(cell):
    """Zwraca tylko pierwszy tekstowy fragment z komórki (ignorując np. nawiasy)."""
    first = cell.find(string=True)
    return first.strip() if first else ''

def scrape_section(stock, section_name, url_path):
    url = BASE_URL.format(url_path.format(stock))
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {
        "class": "report-table",
        "data-report-type": "Y",
    })

    if not table:
        print(f"⚠️  Brak danych dla {stock} w sekcji {section_name}")
        return []

    rows = table.find_all("tr")
    if not rows:
        return []

    # === 1. Wyciąganie nagłówków (Rok)
    header_cells = rows[0].find_all("th")[1:]  # pomijamy pierwszy pusty <th>
    years = [get_first_text(cell) for cell in header_cells]

    # === 2. Wyciąganie dat publikacji z <tr data-field="PrimaryReport">
    pub_row = table.find("tr", {"data-field": "PrimaryReport"})
    pub_dates = []
    if pub_row:
        tds = pub_row.find_all("td")
        for td in tds:
            date = td.get("title", "").strip()
            pub_dates.append(date)
    else:
        pub_dates = [""] * len(years)

    # === 3. Tworzymy rekordy (1 na rok)
    data_by_year = []
    for i in range(len(years)):
        data_by_year.append({
            "Spółka": stock,
            "Rok": years[i],
            "Data publikacji": pub_dates[i] if i < len(pub_dates) else ""
        })

    # === 4. Dodajemy dane wskaźników
    for row in rows[1:]:
        if row.get("data-field") == "PrimaryReport":
            continue  # pomijamy wiersz z datami
        cols = row.find_all(["th", "td"])
        if not cols:
            continue
        metric = get_first_text(cols[0])
        values = [parse_number(get_first_text(col)) for col in cols[1:]]

        for i, val in enumerate(values):
            if i < len(data_by_year):
                data_by_year[i][metric] = val

    # === 5. Filtrowanie pustych wierszy (brak jakichkolwiek wskaźników)
    cleaned = []
    for row in data_by_year:
        values_only = {k: v for k, v in row.items() if k not in ['Spółka', 'Rok']}
        if any(v is not None and v != '' for v in values_only.values()):
            cleaned.append(row)

    return cleaned





def main():
    stock_df = pd.read_csv(stock_list)
    all_data = {
        "zysk": [],
        "bilans": [],
        "przeplywy": [],
    }

    for idx, row in stock_df.iterrows():
        try:
            stock = row['adress'].split('/')[-1]
            print(f"🔄 Przetwarzanie spółki: {stock}")

            for section_name, url_path in SECTIONS.items():
                scraped = scrape_section(stock, section_name, url_path)
                all_data[section_name].extend(scraped)

            time.sleep(2)  # aby nie przeciążyć serwera
        except Exception as e:
            print(f"❌ Błąd przy spółce: {row['adress']}, {e}")

    # Zapisz do CSV – pełna tabela przestawna
    for section_name, data in all_data.items():
        df = pd.DataFrame(data)
        df = df.sort_values(by=["Spółka", "Rok"])
        df.to_csv('Data/' + OUTPUT_FILES[section_name], index=False, encoding='utf-8')
        print(f"✅ Zapisano dane do {OUTPUT_FILES[section_name]} ({len(df)} rekordów)")

if __name__ == "__main__":
    main()
