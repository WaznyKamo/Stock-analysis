import streamlit as st
import pandas as pd
from Sripts.data_preparation import calculate_cagr

st.title("Wyszukiwanie spółek na podstawie średnich rocznych zmian raportowanych danych")
st.write("Narzędzie do identyfikacji spółek o wysokim potencjale rozwoju.")
st.write("Do kalkulacji wykorzystano dane z raportów finansowych oraz miarę średniej rocznej zmiany (CAGR) dla wybranych parametrów.")
st.latex(r"""
\text{CAGR} = \left( \frac{Wartość\ końcowa}{Wartość\ początkowa} \right)^{\frac{1}{liczba\ lat}} - 1
""")
st.write("W przypadku gdy dane są ujemne, nie jest możliwe wyliczenie CAGR. W takim przypadku oraz gdy brakuje danych zostanie zwrócona wartość NaN.")

financial_report = st.session_state.financial_report

window_options = [1, 3, 5, 10, 15, "Brak"]
window = st.selectbox("Okno czasowe: ", window_options, index=0)



cagr_result = calculate_cagr(financial_report, window)
st.write("Wynik funkcji calculate_cagr dla wybranego okna czasowego:")
st.dataframe(cagr_result)
