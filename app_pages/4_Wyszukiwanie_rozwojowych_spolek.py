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
window = st.selectbox("Okno czasowe (w latach): ", window_options, index=0)

cagr_result = calculate_cagr(financial_report, window)
st.write("Filtruj dane po wybranych kolumnach:")

num_cols = cagr_result.select_dtypes(include='number').columns.tolist()

# Inicjalizacja filtrów w session_state
if "growth_filters" not in st.session_state:
    st.session_state.growth_filters = [{
        "col": num_cols[0] if num_cols else "",
        "op": ">=",
        "val": 0.0,
        "active": True  # Dodaj pole aktywności filtra
    }]

# Przycisk odświeżania filtrów pod formularzem
if st.button("🔄 Zresetuj filtry"):
    st.session_state.growth_filters = [{
        "col": num_cols[0] if num_cols else "",
        "op": ">=",
        "val": 0.0,
        "active": True
    }]

# Przycisk dodawania kolejnego filtra
if st.button("➕ Dodaj kolejny filtr") and len(st.session_state.growth_filters) < len(num_cols):
    already_selected = [f["col"] for f in st.session_state.growth_filters if f["col"]]
    remaining_cols = [col for col in num_cols if col not in already_selected]
    st.session_state.growth_filters.append({
        "col": remaining_cols[0] if remaining_cols else num_cols[0],
        "op": ">=",
        "val": 0.0,
        "active": True
    })

with st.form("cagr_filter_form"):
    used_cols = []
    for i, filt in enumerate(st.session_state.growth_filters):
        available_cols = [col for col in num_cols if col not in used_cols or col == filt["col"]]
        col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
        with col1:
            filt["col"] = st.selectbox(
                f"Wskaźnik #{i+1}",
                options=available_cols,
                index=available_cols.index(filt["col"]) if filt["col"] in available_cols else 0,
                key=f"growth_col_{i}"
            )
            used_cols.append(filt["col"])
        with col2:
            filt["op"] = st.selectbox("Funkcja", [">=", "<="], key=f"growth_op_{i}")
        with col3:
            filt["val"] = st.number_input("Wartość", value=filt["val"], key=f"growth_val_{i}")
        with col4:
            filt["active"] = st.checkbox("Uwzględnij", value=filt.get("active", True), key=f"growth_active_{i}")
    submitted = st.form_submit_button("✅ Filtruj")

st.info("Przedstawione dane przedstawiają średnioroczną zmianę wyrażoną w prcentach %")

if submitted:
    filtered = cagr_result.copy()
    for filt in st.session_state.growth_filters:
        if filt["col"] and filt.get("active", True):
            if filt["op"] == ">=":
                filtered = filtered[filtered[filt["col"]] >= filt["val"]]
            else:
                filtered = filtered[filtered[filt["col"]] <= filt["val"]]
    st.dataframe(filtered)
else:
    st.dataframe(cagr_result)
