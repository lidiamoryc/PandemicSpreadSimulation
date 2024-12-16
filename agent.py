import random
import pygame
import math


class Agent:
    def __init__(self, id, x, y, state="S"):
        self.id = id  # Unikalny identyfikator agenta
        self.state = state  # Stan agenta: S, E, I, R, D
        self.x = x  # Pozycja X
        self.y = y  # Pozycja Y
        self.size = 5  # Rozmiar agenta
        self.speed = 2
        self.time_in_state = 0  # Czas spędzony w aktualnym stanie
        self.direction_x, self.direction_y = self.assign_random_direction()
        self.central_location = None
        self.moving_to_central_location = False
        self.moving_out_of_central_location = False
        self.time_to_spend_in_central_location = 0

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
                if random.random() < config.infection_rate:
                    self.update_state("E")  # Zarażenie, przejście do stanu "E"
                    break

    def state_E(self, config):
        """Stan narażony - agent może przejść w stan "I" (zakażony) lub wrócić do zdrowia."""
        if self.time_in_state >= config.incubation_period:
            self.update_state("I")  # Po okresie inkubacji przejście do stanu "I"

    def state_I(self, config):
        """Stan zakażony - agent może wyzdrowieć lub umrzeć."""
        if random.random() < config.recovery_rate and self.time_in_state >= config.recovery_period:
            self.update_state("R")  # Przechodzi do stanu wyzdrowienia
        elif random.random() < config.mortality_rate and self.time_in_state >= config.mortality_period:
            self.update_state("D")  # Umiera

    def state_R(self, config):
        if random.random() < config.immunity_loss_rate and self.time_in_state >= config.immunity_loss_period:
            self.update_state("S")

    def distance_to(self, other_agent):
        """Obliczenie odległości między dwoma agentami."""
        return math.sqrt((self.x - other_agent.x) ** 2 + (self.y - other_agent.y) ** 2)

    def move(self, width, height):
        """Poruszanie agenta po planszy (odbicie od krawędzi)."""
        if self.state == "D":
            return

        if not self.is_in_central_location() and not self.moving_to_central_location:
            self.moving_to_central_location = True
            self.direct_to_central_location()
            return
        elif self.is_in_central_location() and self.moving_to_central_location:
            self.moving_to_central_location = False
            self.direction_x, self.direction_y = self.assign_random_direction()
            self.x = self.central_location.x + self.central_location.size // 2
            self.y = self.central_location.y + self.central_location.size // 2


        self.x += self.direction_x
        self.y += self.direction_y

        agent_in_central_location = not (self.central_location is None or self.moving_to_central_location)

        left_bound_x, right_bound_x, upper_bound_y, bottom_bound_y = 0, width, 0, height
        if agent_in_central_location:
            left_bound_x = self.central_location.x
            right_bound_x = self.central_location.x + self.central_location.size
            upper_bound_y = self.central_location.y
            bottom_bound_y = self.central_location.y + self.central_location.size

        # Odbicie od krawędzi
        if self.x <= left_bound_x or self.x >= right_bound_x - self.size:
            self.direction_x *= -1
        if self.y <= upper_bound_y or self.y >= bottom_bound_y - self.size:
            self.direction_y *= -1


    def direct_to_central_location(self):
        """Skierowanie agenta w kierunku centrum przypisanej do niego Central Location"""

        center_x = self.central_location.x + self.central_location.size // 2
        center_y = self.central_location.y + self.central_location.size // 2

        direction_x = center_x - self.x
        direction_y = center_y - self.y

        self.direction_x = direction_x / 10
        self.direction_y = direction_y / 10


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

    def step(self, agents, config, screen, central_locations, width, height):
        """Aktualizacja agenta: poruszanie się, rysowanie i przejście stanu."""
        self.visit_central_location(config, central_locations)
        self.change_direction(config)
        self.move(width, height)  # Poruszanie
        self.transition(agents, config)  # Aktualizacja stanu
        self.draw(screen, config)  # Rysowanie agenta
        self.increment_time_in_state()  # Zwiększanie licznika czasu w danym stanie

    def visit_central_location(self, config, central_locations):
        if len(central_locations) == 0:
            return

        if self.central_location and self.moving_to_central_location is False:
            self.time_to_spend_in_central_location -= 1
            if self.time_to_spend_in_central_location <= 0:
                self.assign_central_location(None)
            return
        if random.random() < config.central_location_visit_proba:
            self.time_to_spend_in_central_location = config.frames_spent_in_central_location
            self.assign_central_location(random.choice(central_locations))

    def change_direction(self, config):
        if self.moving_to_central_location or self.moving_out_of_central_location:
            return
        if random.random() < config.change_direction_proba:
            self.direction_x, self.direction_y = self.assign_random_direction()

    def assign_central_location(self, central_location):
        self.central_location = central_location

    def is_in_central_location(self):
        if self.central_location is None:
            return True

        return self.central_location.x <= self.x <= self.central_location.x + self.central_location.size and \
            self.central_location.y <= self.y <= self.central_location.y + self.central_location.size

