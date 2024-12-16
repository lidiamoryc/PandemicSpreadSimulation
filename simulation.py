import random
from PIL import Image
import pygame
import math
import matplotlib.pyplot as plt
import time

from agent import Agent
from model import Model
from central_location import CentralLocation


class Simulation:
    def __init__(self, config):
        self.config = config
        self.agents = [Agent(i, random.randint(0, config.width), random.randint(0, config.height)) for i in
                       range(config.num_agents)]
        self.central_locations = [CentralLocation(config.width // 2 - config.central_location_size // 2,
                                                  config.height // 2 - config.central_location_size // 2,
                                                  config.central_location_size)
                                  for _ in range(config.num_central_locations)]
        for i in range(10):
            self.agents[i].update_state("I")
        self.model = Model(config)

        self.state_history = []  # Lista do przechowywania historii stanów

    def run(self, steps, screen, clock, gif_filename):
        """Uruchomienie symulacji przez określoną liczbę kroków i zapisanie do pliku GIF."""
        frames = []  # Lista do przechowywania klatek

        running = True
        while running and steps > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Ustalenie tła i rysowanie agentów
            screen.fill((255, 255, 255))  # Tło białe

            for central_location in self.central_locations:
                central_location.draw(screen)

            self.step(screen)

            # Zapisanie stanu symulacji
            self.record_state()

            # Zapisanie klatki
            frame = pygame.image.tostring(screen, 'RGB')
            image = Image.frombytes('RGB', (self.config.width, self.config.height), frame)
            frames.append(image)

            pygame.display.flip()  # Aktualizacja ekranu
            clock.tick(24)  # Ustalamy ilość klatek na sekundę
            steps -= 1

        # Zapisanie klatek jako GIF
        if frames:
            frames[0].save(gif_filename, save_all=True, append_images=frames[1:], optimize=True, duration=100, loop=0)

        # Rysowanie wykresu
        self.plot_state_history()

        pygame.quit()

    def step(self, screen):
        """Przeprowadzenie jednego kroku symulacji."""
        for agent in self.agents:
            agent.step(self.agents, self.config, screen, self.central_locations, self.config.width,
                       self.config.height)  # Wykonanie kroku dla każdego agenta

    def record_state(self):
        """Zapisuje liczbę agentów w każdym stanie w danym momencie."""
        state_counts = {"S": 0, "E": 0, "I": 0, "R": 0, "D": 0}

        for agent in self.agents:
            state_counts[agent.state] += 1

        # Dodajemy stan do historii
        self.state_history.append(state_counts)

    def plot_state_history(self):
        """Rysowanie wykresu rozkładu stanów w czasie."""
        time_steps = range(len(self.state_history))
        susceptible = [state["S"] for state in self.state_history]
        exposed = [state["E"] for state in self.state_history]
        infected = [state["I"] for state in self.state_history]
        recovered = [state["R"] for state in self.state_history]
        dead = [state["D"] for state in self.state_history]

        # Tworzymy wykres
        plt.figure(figsize=(10, 6))
        plt.plot(time_steps, susceptible, label="S - Susceptible", color="blue")
        plt.plot(time_steps, exposed, label="E - Exposed", color="yellow")
        plt.plot(time_steps, infected, label="I - Infected", color="red")
        plt.plot(time_steps, recovered, label="R - Recovered", color="green")
        plt.plot(time_steps, dead, label="D - Dead", color="black")

        # Dodajemy parametry config do tytułu wykresu
        title = f"Agent States Over Time\n"
        title += f"Num Agents: {self.config.num_agents}, Infection Rate: {self.config.infection_rate}, Recovery Rate: {self.config.recovery_rate}, Minimum Recovery Period: {self.config.recovery_period}, \nMortality Rate: {self.config.mortality_rate}, Minimum Mortality Period: {self.config.mortality_period}, \nImmunity Loss Rate: {self.config.immunity_loss_rate}, Minimum Immunity Loss Period: {self.config.immunity_loss_period}, Infection Radius: {self.config.infection_radius}"
        plt.title(title)

        plt.xlabel("Time Step")
        plt.ylabel("Number of Agents")
        plt.legend()
        plt.grid(True)

        plt.show()
