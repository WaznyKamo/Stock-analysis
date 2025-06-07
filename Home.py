import streamlit as st
from Sripts.data_preparation import prepare_indicator_data, prepare_latest_indicator_data

st.set_page_config(page_title="Aplikacja Finansowa", layout="wide")

# Wczytaj dane tylko raz
if "df_ind" not in st.session_state:
    st.session_state.df_ind = prepare_indicator_data()
if "df_ind_latest" not in st.session_state:
    st.session_state.df_ind_latest = prepare_latest_indicator_data()
    

pages = [
    st.Page("app_pages/1_strona_glowna.py", title="Strona główna", icon="🏠"),
    st.Page("app_pages/2_wizualizacja_wskaznikow.py", title="Wizualizacja wskaźników", icon="📊"),
    st.Page("app_pages/3_wyszukiwanie_jednorozcow.py", title="Wyszukiwanie jednorożców", icon="🦄")
]

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()

# To run this app, use the terminal:
# streamlit run Home.py

