import streamlit as st

st.set_page_config(page_title="Aplikacja Finansowa", layout="wide")

pages = [
    st.Page("app_pages/1_strona_glowna.py", title="Strona główna", icon="🏠"),
    st.Page("app_pages/2_wizualizacja_wskaznikow.py", title="Wizualizacja wskaźników", icon="📊"),
    st.Page("app_pages/3_wyszukiwanie_jednorozcow.py", title="Wyszukiwanie jednorożców", icon="🦄")
]



# st.sidebar.title("📁 Nawigacja")
# st.sidebar.page_link("Home.py", label="🏠 Strona główna")
# st.sidebar.page_link("Pages/1_wizualizacja_wskaznikow.py", label="📊 Wizualizacja wskaźników")
# st.sidebar.page_link("Pages/2_Wyszukiwanie_jednorozcow.py", label="🦄 Wyszukiwanie jednorożców")
pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()
