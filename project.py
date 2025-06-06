import streamlit as st
from Sripts.data_preparation import prepare_price_data, prepare_indicator_data
from Sripts.data_visualisation import plot_multiple_y_axes

# df_price = prepare_price_data()
df_ind = prepare_indicator_data()

st.title("Wykres danych w czasie")

# Panel boczny
st.sidebar.title("Wybierz kolumnę do wyświetlenia")
if st.sidebar.button("🔄 Odśwież"):
    st.session_state.kolumny_wykres = []
    if 'spolka' in st.session_state:
        del st.session_state['spolka']
    st.rerun()

dostepne_spolki = df_ind['Spółka'].unique()
wybrana_spolka = st.sidebar.selectbox("Wybierz spółkę", sorted(dostepne_spolki))
df_ind_filtered = df_ind[df_ind['Spółka'] == wybrana_spolka]



kolumny_danych = [col for col in df_ind.columns if col not in  ['Data', 'Spółka', 'Kwartały']]

st.sidebar.title("Kolumny na wykresie")
if 'kolumny_wykres' not in st.session_state:
    st.session_state.kolumny_wykres = [kolumny_danych[0]]

dodaj_kolumne = st.sidebar.button("➕ Dodaj kolumnę")

if dodaj_kolumne:
    # Dodaj nową kolumnę domyślnie jako pierwszą niewybraną
    niewybrane = [k for k in kolumny_danych if k not in st.session_state.kolumny_wykres]
    if niewybrane:
        st.session_state.kolumny_wykres.append(niewybrane[0])

# Interfejs wyboru kolumn
nowe_kolumny = []
for i, kol in enumerate(st.session_state.kolumny_wykres):
    selected = st.sidebar.selectbox(f"Kolumna {i+1}", kolumny_danych, index=kolumny_danych.index(kol), key=f"kol_{i}")
    nowe_kolumny.append(selected)

# wybrana_kolumna = st.sidebar.selectbox("Kolumna", kolumny_danych)
st.session_state.kolumny_wykres = nowe_kolumny

plot_multiple_y_axes(df_ind_filtered, st.session_state.kolumny_wykres, title_prefix=wybrana_spolka)

# To run this app, use the terminal:
# streamlit run project.py