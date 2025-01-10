class Config:
    def __init__(self):
        self.num_agents = 1000  # Liczba agentów w populacji
        self.infection_rate = 0.03  # Prawdopodobieństwo zarażenia zdrowego agenta
        self.incubation_period = 15  # Prawdopodobieństwo przejścia z narażenia do zakażenia
        self.recovery_rate = 0.3 # Prawdopodobieństwo wyzdrowienia
        self.recovery_period = 30
        self.mortality_rate = 0.007  # Prawdopodobieństwo śmierci
        self.mortality_period = 50
        self.width = 800  # Szerokość planszy
        self.height = 800 # Wysokość planszy
        self.infection_radius = 25  # Promień zakażenia, w którym agent może zarazić innych
        self.initial_infected = 20  # Liczba początkowo zakażonych agentów
        self.immunity_loss_rate = 0.02
        self.immunity_loss_period = 30
        self.change_direction_proba = 0.1

        self.num_central_locations = 1
        self.central_location_size = 100
        self.central_location_visit_proba = 0.005
        self.frames_spent_in_central_location = 50

        self.quarantine = True
        self.quarantine_visit_proba = 0.04

        self.social_distancing_repulsion_force = 0
        self.social_distancing_repulsion_radius = self.infection_radius + 10

        self.mask_wearing_proba = 0.7
        self.vaccinated_proba = 0.5

    def params_values_text(self):
        result = ''
        for variable_name, variable_value in vars(self).items():
            result += f'{variable_name}: {variable_value}\n'
        return result
