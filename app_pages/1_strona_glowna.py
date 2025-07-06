import streamlit as st

st.title("Strona główna")
st.markdown("<h3>Aplikacja jest projektem w fazie intensywnego rozwoju 🏗️</h3>", unsafe_allow_html=True)
st.write("Witaj w aplikacji do analizy spółek. Powstała ona z myślą o inwestorach, którzy chcą lepiej wartość fundamentalną i podejmować świadome, oparte na wynikach finansowych decyzje inwestycyjne.")

st.markdown("<h3>Aktualne moduły: </h3>", unsafe_allow_html=True)
st.markdown("""
- **Wizualizacja wskaźników**
            
    pozwala na zobrazowanie na jednym wykresie wielu danych finansowych spółek. Pozwala to na lepsze zrozumienie zależności między różnymi wskaźnikami finansowymi.
- **Wyszukiwarka niedowartościowanych spółek**
            
    pozwala na odfiltrowanie spółek o podanych wartościach wskaźników finansowych, takich jak Wartość Księgowa na Akcję, Cena do Zysku (C/Z) czy wskaźników dotyczących zadłużenia. Dzięki temu inwestorzy mogą szybko znaleźć spółki, które spełniają ich kryteria inwestycyjne.
- **Wyszukiwarka szybko rozwijających się spółek**
            
    pozwala na identyfikację spółek, które wykazują dynamiczny wzrost w kluczowych wskaźnikach finansowych, takich jak przychody, zysk netto czy EBITDA. Umożliwia to inwestorom znalezienie spółek o wysokim potencjale wzrostu.
""")

st.markdown("<h4>Planowane moduły: </h4>", unsafe_allow_html=True)
st.markdown("""
- **Przegląd danych finansowych wybranych spółek**
""")