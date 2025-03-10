import random
from PIL import Image
import numpy as np
import pygame
import matplotlib.pyplot as plt

from agent import Agent
from functions import age_immunity_loss_proba, age_infection_proba, age_mortality_proba, age_recovery_proba, \
    gender_immunity_loss_proba, gender_infection_proba, gender_mortality_proba, gender_recovery_proba, \
    mask_immunity_loss_proba, mask_infection_proba, mask_mortality_proba, mask_recovery_proba, \
    vaccinated_immunity_loss_proba, vaccinated_infection_proba, vaccinated_mortality_proba, vaccinated_recovery_proba
from model import Model
from central_location import CentralLocation
import math
import os

class Simulation:
    def __init__(self, config):
        self.config = config

        self.quarantine = CentralLocation(config.width - config.central_location_size,
                                          config.height - config.central_location_size,
                                          config.central_location_size) if config.quarantine else None
        self.board_width, self.board_height = (config.width, config.height) if self.quarantine is None \
            else (config.width - self.quarantine.size - config.infection_radius * 2,
                  config.height - self.quarantine.size - config.infection_radius * 2)

        self.agents = [Agent(i, random.randint(0, self.board_width - 10), random.randint(0, self.board_height - 10), config) for i in
                       range(config.num_agents)]
        self.board_grid = []

        self.central_locations = [CentralLocation(self.board_width // 2 - config.central_location_size // 2,
                                                  self.board_height // 2 - config.central_location_size // 2,
                                                  config.central_location_size)
                                  for _ in range(config.num_central_locations)]

        for i in range(config.initial_infected):
            self.agents[i].update_state("I")
        self.model = Model(config)

        self.state_history = []  # Lista do przechowywania historii stanów
        self.dists = self.get_dists()
        self.rates = self.get_rates(config)

    def get_rates(self, config):
        rates = {
            "infection": {},
            "recovery": {},
            "mortality": {},
            "immunity_loss": {}
        }

        for agent in self.agents:
            infection_rate = np.round(agent.compute_infection_rate(config), 2) * 100
            recovery_rate = np.round(agent.compute_recovery_rate(config), 2) * 100
            moratality_rate = np.round(agent.compute_mortality_rate(config), 2) * 100
            immunity_loss_rate = np.round(agent.compute_immunity_loss_rate(config), 2) * 100
            
            if infection_rate in rates["infection"]:
                rates["infection"][infection_rate] += 1
            else:
                rates["infection"][infection_rate] = 1

            if recovery_rate in rates["recovery"]:
                rates["recovery"][recovery_rate] += 1
            else:
                rates["recovery"][recovery_rate] = 1

            if moratality_rate in rates["mortality"]:
                rates["mortality"][moratality_rate] += 1
            else:
                rates["mortality"][moratality_rate] = 1

            if immunity_loss_rate in rates["immunity_loss"]:
                rates["immunity_loss"][immunity_loss_rate] += 1
            else:
                rates["immunity_loss"][immunity_loss_rate] = 1
        
        return rates
    
    def get_dists(self):
        dists = {
            'age': {},
            'gender': {},
            'vaccinated': {},
            'mask': {}
        }

        for agent in self.agents:
            
            if agent.age in dists['age']:
                dists['age'][agent.age] += 1
            else:
                dists['age'][agent.age] = 1

            if agent.gender in dists['gender']:
                dists['gender'][agent.gender] += 1
            else:
                dists['gender'][agent.gender] = 1

            if agent.vaccinated in dists['vaccinated']:
                dists['vaccinated'][agent.vaccinated] += 1
            else:
                dists['vaccinated'][agent.vaccinated] = 1

            if agent.mask in dists['mask']:
                dists['mask'][agent.mask] += 1
            else:
                dists['mask'][agent.mask] = 1

        return dists


    def save_plots(self):
        # Save the state history plot
        self.plot_state_history()
        plt.savefig("plot/state_history_plot.png", dpi=300)  # Save with high resolution
        plt.close()  # Close the plot to avoid overlapping with other plots

        # Save the distributions plot
        self.plot_dists()
        plt.savefig("plot/distributions_plot.png", dpi=300)
        plt.close()

        # # Save the functions plot
        # self.plot_functions()
        # plt.savefig("functions_plot.png", dpi=300)
        # plt.close()

        # Save the rates plot
        self.plot_rates()
        plt.savefig("plot/rates_plot.png", dpi=300)
        plt.close()

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

            if self.quarantine:
                self.quarantine.draw(screen)
                pygame.draw.rect(screen,
                                 (0, 0, 0),
                                 pygame.Rect(0, 0, self.board_width, self.board_height), 2)

            self.step(screen)

            # Zapisanie stanu symulacji
            self.record_state()

            if not os.path.exists('figures'):
                os.makedirs('figures')
            frame = pygame.image.tostring(screen, 'RGB')
            image = Image.frombytes('RGB', (self.config.width, self.config.height), frame)
            frames.append(image)

            # NOTE: odkomentować, jeśli potrzeba wyświelić symulację w oknie pygame
            pygame.display.flip()  # Aktualizacja ekranu
            clock.tick(24)  # Ustalamy ilość klatek na sekundę
            steps -= 1

        # Zapisanie klatek jako GIF
        if frames:
            frames[0].save(gif_filename, save_all=True, append_images=frames[1:], optimize=True, duration=40, loop=0)

        # # Rysowanie wykresów
        # self.plot_state_history()
        # self.plot_dists()
        # self.plot_functions()
        # self.plot_rates()
        #
        # plt.show()

        self.save_plots()

        pygame.quit()

    def step(self, screen):
        """Przeprowadzenie jednego kroku symulacji."""
        self.board_grid = self.build_board_grid()
        for agent in self.agents:
            agent.step(self.config, screen, self.central_locations, self.quarantine,
                       self.board_width, self.board_height, self.board_grid)  # Wykonanie kroku dla każdego agenta

    def build_board_grid(self):
        grid_width = math.ceil(self.board_height / self.config.social_distancing_repulsion_radius)
        grid_height = math.ceil(self.board_width / self.config.social_distancing_repulsion_radius)
        result = [
            [
                [] for _ in range(grid_width)
            ] for _ in range(grid_height)
        ]
        for agent in self.agents:
            i = int(agent.x // self.config.social_distancing_repulsion_radius)
            j = int(agent.y // self.config.social_distancing_repulsion_radius)

            # fallback for the agents that exit the board
            i = i if i < grid_width else grid_width - 1
            j = j if j < grid_width else grid_width - 1
            result[i][j].append(agent)
        return result

    def record_state(self):
        """Zapisuje liczbę agentów w każdym stanie w danym momencie."""
        state_counts = {"S": 0, "E": 0, "I": 0, "R": 0, "D": 0}

        for agent in self.agents:
            state_counts[agent.state] += 1

        # Dodajemy stan do historii
        self.state_history.append(state_counts)

    def plot_dists(self):
        fig, ax = plt.subplots(2, 2, figsize=(10, 5))

        ax[0, 0].bar(self.dists['age'].keys(), self.dists['age'].values(), color="skyblue")
        ax[0, 0].set_title("Age Distribution")
        ax[0, 0].set_xlabel("Age")
        ax[0, 0].set_ylabel("Count")
        ax[0, 0].grid(True)

        ax[0, 1].pie(self.dists['gender'].values(), labels=self.dists['gender'].keys(), autopct='%1.2f%%',
                     startangle=90, colors=["blue", "pink"])
        ax[0, 1].set_title("Gender Distribution")

        ax[1, 0].pie(self.dists['vaccinated'].values(), labels=self.dists['vaccinated'].keys(), autopct='%1.2f%%',
                     startangle=90, colors=["blue", "pink"])
        ax[1, 0].set_title("Vaccination Distribution")

        ax[1, 1].pie(self.dists['mask'].values(), labels=self.dists['mask'].keys(), autopct='%1.2f%%', startangle=90,
                     colors=["blue", "pink"])
        ax[1, 1].set_title("Mask Wearing Distribution")

        plt.tight_layout()
        fig.savefig('figures/distributions.png')

    def plot_functions(self):
        fig1, ax = plt.subplots(2, 4, figsize=(10, 5))
        fig2, ax2 = plt.subplots(2, 4, figsize=(10, 5))

        ages = np.linspace(0, 100)
        genders = ['Male', 'Female']
        vaccinated = ['True', 'False']
        masks = ['True', 'False']

        infection_vals = [age_infection_proba(age) for age in ages]
        ax[0, 0].plot(ages, infection_vals, label="InfectionProbability(age)")
        ax[0, 0].set_xlabel("Age")
        ax[0, 0].set_ylabel("Rate")
        ax[0, 0].legend()
        ax[0, 0].grid(True)

        ax[0, 1].bar(genders, [gender_infection_proba(gender) for gender in genders], color='darkgreen')
        ax[0, 1].set_title("InfectionProbability(gender)")

        ax[0, 2].bar(vaccinated, [vaccinated_infection_proba(vacc) for vacc in vaccinated], color='gray')
        ax[0, 2].set_title("InfectionProbability(vaccinated)")

        ax[0, 3].bar(masks, [mask_infection_proba(mask) for mask in masks], color='red')
        ax[0, 3].set_title("InfectionProbability(wearing_mask)")

        recovery_vals = [age_recovery_proba(age) for age in ages]
        ax[1, 0].plot(ages, recovery_vals, label="RecoveryProbability(age)")
        ax[1, 0].set_xlabel("Age")
        ax[1, 0].set_ylabel("Rate")
        ax[1, 0].legend()
        ax[1, 0].grid(True)

        ax[1, 1].bar(genders, [gender_recovery_proba(gender) for gender in genders], color='darkgreen')
        ax[1, 1].set_title("RecoveryProbability(gender)")

        ax[1, 2].bar(vaccinated, [vaccinated_recovery_proba(vacc) for vacc in vaccinated], color='gray')
        ax[1, 2].set_title("RecoveryProbability(vaccinated)")

        ax[1, 3].bar(masks, [mask_recovery_proba(mask) for mask in masks], color='red')
        ax[1, 3].set_title("RecoveryProbability(wearing_mask)")

        mortality_vals = [age_mortality_proba(age) for age in ages]
        ax2[0, 0].plot(ages, mortality_vals, label="MortalityProbability(age)")
        ax2[0, 0].set_xlabel("Age")
        ax2[0, 0].set_ylabel("Rate")
        ax2[0, 0].legend()
        ax2[0, 0].grid(True)

        ax2[0, 1].bar(genders, [gender_mortality_proba(gender) for gender in genders], color='darkgreen')
        ax2[0, 1].set_title("MortalityProbability(gender)")

        ax2[0, 2].bar(vaccinated, [vaccinated_mortality_proba(vacc) for vacc in vaccinated], color='gray')
        ax2[0, 2].set_title("MortalityProbability(vaccinated)")

        ax2[0, 3].bar(masks, [mask_mortality_proba(mask) for mask in masks], color='red')
        ax2[0, 3].set_title("MortalityProbability(wearing_mask)")

        immunity_loss_vals = [age_immunity_loss_proba(age) for age in ages]
        ax2[1, 0].plot(ages, immunity_loss_vals, label="ImmunityLossProbability(age)")
        ax2[1, 0].set_xlabel("Age")
        ax2[1, 0].set_ylabel("Rate")
        ax2[1, 0].legend()
        ax2[1, 0].grid(True)

        ax2[1, 1].bar(genders, [gender_immunity_loss_proba(gender) for gender in genders], color='darkgreen')
        ax2[1, 1].set_title("ImmunityLossProbability(gender)")

        ax2[1, 2].bar(vaccinated, [vaccinated_immunity_loss_proba(vacc) for vacc in vaccinated], color='gray')
        ax2[1, 2].set_title("ImmunityLossProbability(vaccinated)")

        ax2[1, 3].bar(masks, [mask_immunity_loss_proba(mask) for mask in masks], color='red')
        ax2[1, 3].set_title("ImmunityLossProbability(wearing_mask)")

        fig1.savefig('figures/functions1.png')
        fig2.savefig('figures/functions2.png')

    def plot_rates(self):
        fig, ax = plt.subplots(1, 4, figsize=(15, 10))

        ax[0].bar(self.rates["infection"].keys(), self.rates["infection"].values(), color="red")
        ax[0].set_title("Infection Rates Distribution")
        ax[0].set_xlabel("Infection Rate (%)")
        ax[0].set_ylabel("Rate")
        ax[0].grid(True)

        ax[1].bar(self.rates["recovery"].keys(), self.rates["recovery"].values(), color="green")
        ax[1].set_title("Recovery Rates Distribution")
        ax[1].set_xlabel("Recovery Rate (%)")
        ax[1].set_ylabel("Rate")
        ax[1].grid(True)

        ax[2].bar(self.rates["mortality"].keys(), self.rates["mortality"].values(), color="black")
        ax[2].set_title("Mortality Rates Distribution")
        ax[2].set_xlabel("Mortality Rate (%)")
        ax[2].set_ylabel("Rate")
        ax[2].grid(True)

        ax[3].bar(self.rates["immunity_loss"].keys(), self.rates["immunity_loss"].values(), color="blue")
        ax[3].set_title("Immunity Loss Rates Distribution")
        ax[3].set_xlabel("Immunity Loss Rate (%)")
        ax[3].set_ylabel("Rate")
        ax[3].grid(True)

        fig.savefig('figures/rates_distribution.png')

    def plot_state_history(self):
        """Rysowanie wykresu rozkładu stanów w czasie."""
        time_steps = range(len(self.state_history))
        susceptible = [state["S"] for state in self.state_history]
        exposed = [state["E"] for state in self.state_history]
        infected = [state["I"] for state in self.state_history]
        recovered = [state["R"] for state in self.state_history]
        dead = [state["D"] for state in self.state_history]

        # Tworzymy wykres
        f, ax = plt.subplots(1, 1, figsize=(15, 6))
        plt.plot(time_steps, susceptible, label="S - Susceptible", color="blue")
        plt.plot(time_steps, exposed, label="E - Exposed", color="yellow")
        plt.plot(time_steps, infected, label="I - Infected", color="red")
        plt.plot(time_steps, recovered, label="R - Recovered", color="green")
        plt.plot(time_steps, dead, label="D - Dead", color="black")

        # Dodajemy parametry config do tytułu wykresu
        title = f"Agent States Over Time"
        plt.title(title)

        plt.xlabel("Time Step")
        plt.ylabel("Number of Agents")
        plt.legend()
        plt.grid(True)

        text = 'Configuration parameters:\n' + self.config.params_values_text()
        box = dict(boxstyle='round', facecolor='grey', alpha=0.15)
        ax.text(1.03, 0.98, text, transform=ax.transAxes, fontsize=8, verticalalignment='top', bbox=box)
        plt.tight_layout()
        plt.savefig('figures/agent_state_history.png')
