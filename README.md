# Symulacja Rozprzestrzeniania Pandemii

## Opis projektu

Celem projektu jest stworzenie narzędzia umożliwiającego symulację rozprzestrzeniania się pandemii w oparciu o dyskretny model systemowy. Symulacja ma na celu badanie wpływu kluczowych parametrów epidemiologicznych oraz skuteczności różnych strategii prewencyjnych na dynamikę pandemii. Projekt dostarcza zarówno możliwości analizy retrospektywnej na podstawie danych historycznych, jak i prognozowania skutków wprowadzania nowych polityk zdrowotnych.

## Funkcjonalności

- Uwzględnienie kluczowych parametrów, takich jak:
  - Zagęszczenie ludności
  - Struktura demograficzna społeczeństwa
  - Działania prewencyjne (szczepienia, maseczki ochronne, dystans społeczny, kwarantanna, praca i nauka zdalna)
- Możliwość symulacji w różnych scenariuszach
- Wsparcie dla analizy retrospektywnej i prognozowania
- Elastyczność w modyfikacji parametrów dla szerokiego zakresu badań naukowych

## Technologie

- **Backend**: Python (z wykorzystaniem biblioteki `pygame` do wizualizacji symulacji)
- **Frontend**: Streamlit (interfejs użytkownika umożliwiający kontrolę parametrów symulacji)

## Struktura projektu

1. **Model formalny**
   - Zaimplementowany w Pythonie, uwzględniający parametry epidemiologiczne oraz różnorodne działania prewencyjne.

2. **Frontend**
   - Streamlit zapewnia prosty i intuicyjny interfejs do sterowania symulacją oraz prezentacji wyników.

3. **Wyniki symulacji**
   - Prezentowane w formie wizualizacji i wykresów umożliwiających łatwą interpretację.

## Uruchamianie projektu

1. **Backend**:
   Aby uruchomić symulację, należy:
   ```bash
   python main.py
   ```

2. **Frontend**:
   TODO

## Wymagania systemowe

- Python 3.8+
- Biblioteki:
  - pygame
  - streamlit
  - numpy
  - pandas

Aby zainstalować wymagane biblioteki, użyj polecenia:
```bash
pip install -r requirements.txt
```

