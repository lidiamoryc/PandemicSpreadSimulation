import streamlit as st
import json

def simulation():
    """Wyświetla zapisane parametry na nowej stronie."""
    st.title("Zapisano! Oto Twoje wartości:")
    try:
        with open("parameters.json", "r") as file:
            parameters = json.load(file)
            for key, value in parameters.items():
                st.write(f"**{key}**: {value}")
    except FileNotFoundError:
        st.error("Nie znaleziono pliku z zapisanymi parametrami.")
