import streamlit as st
import json

def save_parameters(s, i, r, d, v):
    """Zapisuje parametry do pliku JSON."""
    parameters = {
        "S": s,
        "I": i,
        "R": r,
        "D": d,
        "V": v
    }
    with open("parameters.json", "w") as file:
        json.dump(parameters, file, indent=4)

def main_page():
    """Funkcja obsługująca główną stronę aplikacji."""
    st.markdown(
        """<style>
        .full-width-button {
            display: block;
            width: 100%;
            margin-top: 20px;
        }
        </style>""",
        unsafe_allow_html=True,
    )

    st.title("Symulacje systemów dyskretnych \n NA PODSTAWIE SYMULACJI ROZPRZESTRZENIANIA SIĘ PANDEMII")

    st.write(""" Symulacja będzie oparta na rozszerzonym modelu SIR:
        **S (Susceptible)**: Osoby podatne na zakażenie,
        **I (Infectious)**: Osoby zakażone, zdolne do przenoszenia choroby,
        **R (Recovered)**: Osoby wyleczone z trwałą odpornością lub odpornością czasową,
        **D (Deceased)**: Osoby, które zmarły w wyniku choroby oraz,
        **V (Vaccinated)**: Osoby zaszczepione, z różnym poziomem ochrony (pełna odporność, częściowa, brak odporności).
        """
    )
    
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Parametry:")
        st.write("S - liczba podatnych na zakażenie")
        st.write("I - liczba zakażonych")
        st.write("R - liczba wyleczonych")
        st.write("D - liczba zmarłych")
        st.write("V - liczba zaszczepionych")

    with col2:
        s_value = st.number_input("Liczba podatnych na zakażenie (S)", min_value=0, step=1, key="s_input")
        i_value = st.number_input("Liczba zakażonych (I)", min_value=0, step=1, key="i_input")
        r_value = st.number_input("Liczba wyleczonych (R)", min_value=0, step=1, key="r_input")
        d_value = st.number_input("Liczba zmarłych (D)", min_value=0, step=1, key="d_input")
        v_value = st.number_input("Liczba zaszczepionych (V)", min_value=0, step=1, key="v_input")

    if st.button("Rozpocznij", key="start_button"):
        save_parameters(s_value, i_value, r_value, d_value, v_value)
        st.session_state["page"] = "next"
