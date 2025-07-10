import streamlit as st
from Sripts.data_preparation import prepare_indicator_data
from Sripts.data_visualisation import plot_multiple_y_axes

# st.set_page_config(page_title="Wizualizacja wskaźników", layout="wide")

# all_data = prepare_indicator_data()

if "all_data" not in st.session_state or st.session_state.all_data.empty:
    st.warning("Brak danych do wyświetlenia.")
else:
    all_data = st.session_state.all_data

st.title("Wizualizacja wskaźników")

col1, col2 = st.columns([1, 3])  # lewa kolumna na wybór, prawa na wykres

with col1:
    st.header("Wybierz dane")

    

    dostepne_spolki = all_data['Nazwa'].unique()
    wybrana_spolka = st.selectbox("Wybierz spółkę", sorted(dostepne_spolki))
    all_data_filtered = all_data[all_data['Nazwa'] == wybrana_spolka]

    kolumny_danych = [col for col in all_data.columns if col not in  ['Data', 'Ticker', 'Kwartały', 'Nazwa']]

    if 'kolumny_wykres' not in st.session_state:
        st.session_state.kolumny_wykres = [kolumny_danych[0]]


    if st.button("➕ Dodaj informację na wykresie"):
        niewybrane = [k for k in kolumny_danych if k not in st.session_state.kolumny_wykres]
        if niewybrane:
            st.session_state.kolumny_wykres.append(niewybrane[0])

    nowe_kolumny = []
    for i, kol in enumerate(st.session_state.kolumny_wykres):
        selected = st.selectbox(f"Kolumna {i+1}", kolumny_danych, index=kolumny_danych.index(kol), key=f"kol_{i}")
        nowe_kolumny.append(selected)


    st.session_state.kolumny_wykres = nowe_kolumny



    if st.button("🔄 Zresetuj wykres"):
        st.session_state.kolumny_wykres = []
        if 'spolka' in st.session_state:
            del st.session_state['spolka']
        st.rerun()

with col2:
    st.info("Poniższy wykres jest interaktywny. Zaznaczenie pola pozwala przybliżyć dane. Podwójne kliknięcie przywraca widok początkowy.")
    st.subheader(f"Wykres: {wybrana_spolka}")
    plot_multiple_y_axes(all_data_filtered, st.session_state.kolumny_wykres, title_prefix="Wskaźniki")