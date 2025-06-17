import streamlit as st
from Sripts.data_preparation import prepare_indicator_data
from Sripts.data_visualisation import plot_multiple_y_axes

# st.set_page_config(page_title="Wizualizacja wskaźników", layout="wide")

df_ind = prepare_indicator_data()

st.title("📊 Wizualizacja wskaźników")

col1, col2 = st.columns([1, 3])  # lewa kolumna na wybór, prawa na wykres

with col1:
    st.header("Wybierz dane")

    

    dostepne_spolki = df_ind['Spółka'].unique()
    wybrana_spolka = st.selectbox("Wybierz spółkę", sorted(dostepne_spolki))
    df_ind_filtered = df_ind[df_ind['Spółka'] == wybrana_spolka]

    kolumny_danych = [col for col in df_ind.columns if col not in  ['Data', 'Spółka', 'Kwartały']]

    if 'kolumny_wykres' not in st.session_state:
        st.session_state.kolumny_wykres = [kolumny_danych[0]]


    if st.button("➕ Dodaj kolumnę"):
        niewybrane = [k for k in kolumny_danych if k not in st.session_state.kolumny_wykres]
        if niewybrane:
            st.session_state.kolumny_wykres.append(niewybrane[0])

    nowe_kolumny = []
    for i, kol in enumerate(st.session_state.kolumny_wykres):
        selected = st.selectbox(f"Kolumna {i+1}", kolumny_danych, index=kolumny_danych.index(kol), key=f"kol_{i}")
        nowe_kolumny.append(selected)


    st.session_state.kolumny_wykres = nowe_kolumny



    if st.button("🔄 Odśwież"):
        st.session_state.kolumny_wykres = []
        if 'spolka' in st.session_state:
            del st.session_state['spolka']
        st.rerun()

with col2:
    st.subheader(f"Wykres: {wybrana_spolka}")
    plot_multiple_y_axes(df_ind_filtered, st.session_state.kolumny_wykres, title_prefix="Wskaźniki")