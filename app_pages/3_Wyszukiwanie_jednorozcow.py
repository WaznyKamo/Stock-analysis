import streamlit as st

# st.set_page_config(page_title="Wyszukiwanie jednorożców")

st.title("🦄 Wyszukiwanie jednorożców")
st.write("Narzędzie do identyfikacji spółek o wysokim potencjale wzrostu.")

# Wyświetl dane z df_ind_latest
if "df_ind_latest" not in st.session_state or st.session_state.df_ind_latest.empty:
    st.warning("Brak danych do wyświetlenia.")
else:
    df_ind_latest = st.session_state.df_ind_latest

    # Filtrowanie
    st.subheader("Filtruj dane")
    num_cols = df_ind_latest.select_dtypes(include='number').columns.tolist()

    with st.form("filter_form"):
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            selected_col = st.selectbox("Nazwa wskaźnika", num_cols)
        with col2:
            operator = st.selectbox("Funkcja", [">=", "<="])
        with col3:
            value = st.number_input("Wartość", value=0.0)
        submitted = st.form_submit_button("Filtruj")

    if submitted:
        if operator == ">=":
            filtered_df = df_ind_latest[df_ind_latest[selected_col] >= value]
        else:
            filtered_df = df_ind_latest[df_ind_latest[selected_col] <= value]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df_ind_latest)