import random
import pygame
import math
import numpy as np

from functions import age_immunity_loss_proba, age_infection_proba, age_mortality_proba, age_recovery_proba, gender_immunity_loss_proba, gender_infection_proba, gender_mortality_proba, gender_recovery_proba, mask_immunity_loss_proba, mask_infection_proba, mask_mortality_proba, mask_recovery_proba, vaccinated_immunity_loss_proba, vaccinated_infection_proba, vaccinated_mortality_proba, vaccinated_recovery_proba


class Agent:
    def __init__(self, id, x, y, state="S"):
        self.id = id  # Unikalny identyfikator agenta
        self.state = state  # Stan agenta: S, E, I, R, D
        self.x = x  # Pozycja X
        self.y = y  # Pozycja Y
        self.destination_x = 0
        self.destination_y = 0   # Użyte do quick travel
        self.size = 5  # Rozmiar agenta
        self.speed = 2
        self.time_in_state = 0  # Czas spędzony w aktualnym stanie
        self.direction_x, self.direction_y = self.assign_random_direction()
        self.central_location = None
        self.quick_travelling = False
        self.quick_travelling_counter = 0
        self.quick_travel_frames = 15
        self.time_to_spend_in_central_location = 0
        self.quarantined = False
        
        self.age = self.assign_age()
        self.gender = self.assign_gender()
        self.vaccinated = self.assign_vaccination()
        self.mask = self.assign_mask()

    def assign_age(self, mean=40, std_dev=10):
        return max(0, int(np.random.normal(mean, std_dev)))
    
    def assign_gender(self):
        gender_value = np.random.uniform(-1, 1)
        return 'Male' if gender_value < 0 else 'Female'
    
    def assign_vaccination(self):
        vaccinated_value = np.random.uniform(-1, 1)
        return 'True' if vaccinated_value < 0 else 'False'
    
    def assign_mask(self):
        mask_value = np.random.uniform(-1, 1)
        return 'True' if mask_value < 0 else 'False'
    
    def compute_infection_rate(self, config):
        return max(0, min(config.infection_rate + age_infection_proba(self.age) + gender_infection_proba(self.gender) + vaccinated_infection_proba(self.vaccinated) + mask_infection_proba(self.mask), 1))
    
    def compute_recovery_rate(self, config):
        return max(0, min(config.recovery_rate + age_recovery_proba(self.age) + gender_recovery_proba(self.gender) + vaccinated_recovery_proba(self.vaccinated) + mask_recovery_proba(self.mask), 1))
    
    def compute_mortality_rate(self, config):
        return max(0, min(config.mortality_rate + age_mortality_proba(self.age) + gender_mortality_proba(self.gender) + vaccinated_mortality_proba(self.vaccinated) + mask_mortality_proba(self.mask), 1))
    
    def compute_immunity_loss_rate(self, config):
        return max(0, min(config.immunity_loss_rate + age_immunity_loss_proba(self.age) + gender_immunity_loss_proba(self.gender) + vaccinated_immunity_loss_proba(self.vaccinated) + mask_immunity_loss_proba(self.mask), 1))

    def assign_random_direction(self):
        vector_length = 0

        while vector_length == 0.0:
            distance_x = random.uniform(-1, 1)
            distance_y = random.uniform(-1, 1)

            vector_length = (distance_x**2 + distance_y**2)**0.5
            if vector_length == 0:
                continue

            distance_x /= vector_length
            distance_x *= self.speed

            distance_y /= vector_length
            distance_y *= self.speed

            return distance_x, distance_y


    def update_state(self, new_state):
        """Zaktualizowanie stanu agenta i resetowanie czasu w danym stanie."""
        self.state = new_state
        self.time_in_state = 0  # Resetowanie licznika czasu w danym stanie

    def increment_time_in_state(self):
        """Zwiększenie czasu spędzonego w danym stanie."""
        self.time_in_state += 1

    def transition(self, agents, config):
        """Aktualizowanie stanu agenta na podstawie jego obecnego stanu i interakcji."""
        if self.state == "S":
            self.state_S(agents, config)
        elif self.state == "E":
            self.state_E(config)
        elif self.state == "I":
            self.state_I(config)
        elif self.state == "R":
            self.state_R(config)
        elif self.state == "D":
            pass  # Zmarli nie zmieniają stanu

    def state_S(self, agents, config):
        """Stan zdrowy - agent może się zarazić."""
        for other_agent in agents:
            if other_agent.state == "I" and self.distance_to(other_agent) < config.infection_radius:
                if random.random() < self.compute_infection_rate(config):
                    self.update_state("E")  # Zarażenie, przejście do stanu "E"
                    break

    def state_E(self, config):
        """Stan narażony - agent może przejść w stan "I" (zakażony) lub wrócić do zdrowia."""
        if self.time_in_state >= config.incubation_period:
            self.update_state("I")  # Po okresie inkubacji przejście do stanu "I"

    def state_I(self, config):
        """Stan zakażony - agent może wyzdrowieć lub umrzeć."""
        if random.random() < self.compute_recovery_rate(config) and self.time_in_state >= config.recovery_period:
            self.update_state("R")  # Przechodzi do stanu wyzdrowienia
        elif random.random() < self.compute_mortality_rate(config) and self.time_in_state >= config.mortality_period:
            self.update_state("D")  # Umiera

    def state_R(self, config):
        if random.random() < self.compute_immunity_loss_rate(config) and self.time_in_state >= config.immunity_loss_period:
            self.update_state("S")

    def distance_to(self, other_agent):
        """Obliczenie odległości między dwoma agentami."""
        return math.sqrt((self.x - other_agent.x) ** 2 + (self.y - other_agent.y) ** 2)

    def move(self, width, height):
        """Poruszanie agenta po planszy (odbicie od krawędzi)."""
        if self.state == "D":
            return

        if self.quick_travelling:
            self.quick_travelling_counter += 1

            if self.quick_travelling_counter >= self.quick_travel_frames:
                self.quick_travelling = False
                self.x, self.y = self.destination_x, self.destination_y
                self.direction_x, self.direction_y = self.assign_random_direction()

        self.x += self.direction_x
        self.y += self.direction_y

        if self.quick_travelling:
            return

        agent_in_central_location = self.central_location is not None

        left_bound_x, right_bound_x, upper_bound_y, bottom_bound_y = 0, width, 0, height
        if agent_in_central_location:
            left_bound_x = self.central_location.x
            right_bound_x = self.central_location.x + self.central_location.size
            upper_bound_y = self.central_location.y
            bottom_bound_y = self.central_location.y + self.central_location.size

        # Odbicie od krawędzi
        if self.x <= left_bound_x + self.size or self.x >= right_bound_x - self.size:
            self.direction_x *= -1
            self.x += self.direction_x * 2
        if self.y <= upper_bound_y + self.size or self.y >= bottom_bound_y - self.size:
            self.direction_y *= -1
            self.y += self.direction_y * 2


    def direct_to_central_location(self):
        """Skierowanie agenta w kierunku centrum przypisanej do niego Central Location"""

        center_x = self.central_location.x + self.central_location.size // 2
        center_y = self.central_location.y + self.central_location.size // 2

        self.quick_travel_to_coordinates(center_x, center_y)

    def quick_travel_to_coordinates(self, x, y):
        """Skierowanie agenta w kierunku określonym przez współrzędne. Agent będzie przemieszczał się bardzo szybko -
        funkcja użyta w przypadku skierowania agenta do CentralLocation/Quarantine, albo do wychodzenia z nich"""

        self.destination_x, self.destination_y = x, y
        direction_x = x - self.x
        direction_y = y - self.y

        self.direction_x = direction_x / self.quick_travel_frames
        self.direction_y = direction_y / self.quick_travel_frames
        self.quick_travelling_counter = 0
        self.quick_travelling = True

    def change_direction(self, config):
        if self.quick_travelling:
            return
        if random.random() < config.change_direction_proba:
            self.direction_x, self.direction_y = self.assign_random_direction()

    def visit_central_location(self, config, central_locations, width, height):
        if len(central_locations) == 0 or self.quarantined:
            return

        if self.central_location and self.quick_travelling is False:
            self.time_to_spend_in_central_location -= 1
            if self.time_to_spend_in_central_location <= 0:
                self.assign_central_location(None, width, height)
            return
        if random.random() < config.central_location_visit_proba:
            self.time_to_spend_in_central_location = config.frames_spent_in_central_location
            self.assign_central_location(random.choice(central_locations), width, height)

    def assign_central_location(self, central_location, width, height):
        self.central_location = central_location
        if central_location is None:
            self.destination_x, self.destination_y = random.randint(0, width), random.randint(0, height)
            self.quick_travel_to_coordinates(self.destination_x, self.destination_y)
        else:
            self.direct_to_central_location()

    def visit_quarantine(self, config, quarantine, width, height):
        if not config.quarantine:
            return
        if self.state == 'I' and not self.quarantined and random.random() < config.quarantine_visit_proba:
            self.quarantined = True
            self.assign_central_location(quarantine, width, height)
        elif self.state == 'R' and self.quarantined:
            self.quarantined = False
            self.assign_central_location(None, width, height)

    def draw(self, screen, config):
        """Rysowanie agenta na ekranie."""
        color = self.get_color()
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)
        # pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), config.infection_radius, 1)  # Rysowanie promienia zakażenia

    def get_color(self):
        """Zwraca kolor agenta w zależności od jego stanu."""
        if self.state == "S":
            return (0, 0, 255)
        elif self.state == "E":
            return (255, 255, 0)
        elif self.state == "I":
            return (255, 0, 0)
        elif self.state == "R":
            return (0, 255, 0)
        elif self.state == "D":
            return (0, 0, 0)

    def step(self, agents, config, screen, central_locations, quarantine, width, height):
        """Aktualizacja agenta: poruszanie się, rysowanie i przejście stanu."""
        self.visit_central_location(config, central_locations, width, height)
        self.visit_quarantine(config, quarantine, width, height)
        self.change_direction(config)
        self.move(width, height)  # Poruszanie
        self.transition(agents, config)  # Aktualizacja stanu
        self.draw(screen, config)  # Rysowanie agenta
        self.increment_time_in_state()  # Zwiększanie licznika czasu w danym stanie
