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
        self.time_in_state = 0  # Czas spędzony w aktualnym stanie
        self.direction_x = random.choice([-1, 1]) * 1.7  # Losowy kierunek poruszania się w poziomie
        self.direction_y = random.choice([-1, 1]) * 1.7  # Losowy kierunek poruszania się w pionie

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
        if self.state == "D":
            return

        """Poruszanie agenta po planszy (odbicie od krawędzi)."""
        self.x += self.direction_x
        self.y += self.direction_y

        # Odbicie od krawędzi
        if self.x <= 0 or self.x >= width - self.size:
            self.direction_x *= -1
        if self.y <= 0 or self.y >= height - self.size:
            self.direction_y *= -1

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

    def step(self, agents, config, screen, width, height):
        """Aktualizacja agenta: poruszanie się, rysowanie i przejście stanu."""
        self.move(width, height)  # Poruszanie
        self.transition(agents, config)  # Aktualizacja stanu
        self.draw(screen, config)  # Rysowanie agenta
        self.increment_time_in_state()  # Zwiększanie licznika czasu w danym stanie
