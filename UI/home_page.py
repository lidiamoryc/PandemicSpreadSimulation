import streamlit as st
import json
import subprocess

def save_parameters(number_of_agents, infection_rate, initial_infected, recovery_period, quarantine_visit_proba):
    """Zapisuje parametry do pliku JSON."""
    parameters = {
        "number_of_agents": number_of_agents,
        "infection_rate": infection_rate,
        "initial_infected": initial_infected,
        "recovery_period": recovery_period,
        "quarantine_visit_proba": quarantine_visit_proba
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

    st.title("Symulacje Systemów Dyskretnych \n NA PODSTAWIE SYMULACJI ROZPRZESTRZENIANIA SIĘ PANDEMII")

    st.write(""" Symulacja będzie oparta na rozszerzonym modelu SEIRD:
            **S (Susceptible)**: Osoby podatne na zakażenie,
            **E (Exposed)**: Osoby narażone na kontakt z patogenem, będące w okresie inkubacji,
            **I (Infectious)**: Osoby zakażone, zdolne do przenoszenia choroby,
            **R (Recovered)**: Osoby wyleczone z trwałą odpornością lub odpornością czasową,
            **D (Deceased)**: Osoby, które zmarły w wyniku choroby.
            """)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Parametry:")

    with col2:
        # Ensure that infection_rate_value is a float between 0 and 1
        number_of_agents_value = st.number_input("Liczba agentów", min_value=0, step=1, key="number_of_agents_input")
        infection_rate_value = st.number_input(
            "Prawdopodobieństwo zarażenia zdrowego agenta",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.2f",
            key="infection_rate_input"
        )
        initial_infected_value = st.number_input("Liczba początkowo zakażonych agentów", min_value=0, step=1, key="initial_infected_input")
        recovery_period_value = st.number_input("Czas potrzebny na wyzdrowienie", min_value=0, step=1, key="recovery_period_input")
        quarantine_visit_proba_value = st.number_input(
            "Prawdopodobieństwo poddania się kwarantannie",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.2f",
            key="quarantine_visit_proba_input"
        )

    def run_simulation(script_path):
        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                check=True
            )
            st.success("Symulacja została uruchomiona pomyślnie!")
            st.text(result.stdout)
        except subprocess.CalledProcessError as e:
            st.error("Wystąpił błąd podczas uruchamiania symulacji:")
            st.text(f"Status: {e.returncode}")
            st.text(f"Błąd: {e.stderr}")
        except FileNotFoundError:
            st.error("Nie znaleziono pliku symulacji. Sprawdź ścieżkę.")

    if st.button("Rozpocznij", key="start_button"):
        save_parameters(number_of_agents_value, infection_rate_value, initial_infected_value, recovery_period_value, quarantine_visit_proba_value)
        st.session_state["page"] = "next"
