import pygame

from config import Config
from simulation import Simulation


if __name__ == "__main__":
    pygame.init()
    config = Config()
    simulation = Simulation(config)
    screen = pygame.display.set_mode((config.width, config.height))
    clock = pygame.time.Clock()

    simulation.run(500, screen, clock, "vis1.gif")  # Uruchamiamy symulację przez 100 kroków
