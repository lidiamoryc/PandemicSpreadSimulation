import streamlit as st
from home_page import main_page
from simulation import simulation

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "main"

    if st.session_state["page"] == "main":
        main_page()

    elif st.session_state["page"] == "next":
        simulation()

        if st.button("Back to Main Page"):
            st.session_state["page"] = "main"


if __name__ == "__main__":
    main()
