import streamlit as st
import pandas as pd

st.title("Wyszukiwanie niedowartościowanych spółek")
st.write("Narzędzie do identyfikacji spółek o wysokim potencjale wzrostu.")

# Inicjalizacja filtrów
if "filters" not in st.session_state:
    st.session_state.filters = [{"col": "", "op": ">=", "val": 0.0}]

indicators = st.session_state.indicators
all_numeric_cols = indicators.select_dtypes(include='number').columns.tolist()

st.subheader("Filtruj dane")

# Przycisk resetowania filtrów (poza formularzem)
if st.button("🔄 Odśwież"):
    st.session_state.filters = [{"col": "", "op": ">=", "val": 0.0}]

# Przycisk dodawania nowego filtra (poza formularzem)
already_selected = [f["col"] for f in st.session_state.filters if f["col"]]
remaining_cols = [col for col in all_numeric_cols if col not in already_selected]
if st.button("➕ Dodaj nowy wskaźnik") and remaining_cols:
    st.session_state.filters.append({"col": "", "op": ">=", "val": 0.0})

# Formularz z filtrami
with st.form("filter_form"):
    used_cols = []
    for i, filt in enumerate(st.session_state.filters):
        available_cols = [col for col in all_numeric_cols if col not in used_cols or col == filt["col"]]
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            filt["col"] = st.selectbox(
                f"Wskaźnik #{i+1}",
                options=available_cols,
                index=available_cols.index(filt["col"]) if filt["col"] in available_cols else 0,
                key=f"col_{i}"
            )
            used_cols.append(filt["col"])
        with col2:
            filt["op"] = st.selectbox("Funkcja", [">=", "<="], key=f"op_{i}")
        with col3:
            filt["val"] = st.number_input("Wartość", value=filt["val"], key=f"val_{i}")

    submitted = st.form_submit_button("✅ Filtruj")

# Filtrowanie danych
if submitted:
    filtered_df = indicators.copy()
    for filt in st.session_state.filters:
        if filt["col"]:
            if filt["op"] == ">=":
                filtered_df = filtered_df[filtered_df[filt["col"]] >= filt["val"]]
            else:
                filtered_df = filtered_df[filtered_df[filt["col"]] <= filt["val"]]
    st.dataframe(filtered_df)
else:
    st.dataframe(indicators)
