import streamlit as st
from Sripts.data_preparation import prepare_indicator_data

st.set_page_config(page_title="Aplikacja Finansowa", layout="wide")

# Wczytaj dane tylko raz
if "df_ind" not in st.session_state:
    st.session_state.all_data, st.session_state.income_yearly, st.session_state.indicators = prepare_indicator_data()



pages = [
    st.Page("app_pages/1_strona_glowna.py", title="Strona główna", icon="🏠"),
    st.Page("app_pages/2_wizualizacja_wskaznikow.py", title="Wizualizacja wskaźników", icon="📊"),
    st.Page("app_pages/3_Wyszukiwanie_niedowartosciowanych_spolek.py", title="Wyszukiwanie niedowartościowanych spółek", icon="🕵️‍♂️")
]

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()

# TODO:
# Pozyskiwanie danych:
#  - pobieranie sektora (pobrany, ale nie dodany do danych)
#  - pobieranie pozostałych danych - bilans i przepływy pieniężne
#  - wyliczenie danych sektorowych
#  - pobieranie wskaźników technicznych

# Wizualizacja wskaźników:
#  - dodanie nazw spółek do wyszukiwarki
#  - przegląd dostępnych danych

# Wyszukiwarka niedoszacowanych spółek:
#  - możliwość filtrowania po wielu wskaźnikach

# Wyszukiwarka szybko rozwijających się spółek:
#  - wybranie wskaźników do analizy
#  - wyliczenie zmiany wskaźników r/r, k/k
#  - możliwość filtrowania po zmianach na wskaźnikach
