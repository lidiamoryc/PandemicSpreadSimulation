import pygame
from config import Config
from simulation import Simulation


if __name__ == "__main__":
    pygame.init()
    config = Config()
    simulation = Simulation(config)

    screen = pygame.Surface((config.width, config.height))
    clock = pygame.time.Clock()

    # NOTE: odkomentować, jeśli potrzeba wyświelić symulację w oknie pygame
    screen = pygame.display.set_mode((config.width, config.height))

    simulation.run(10, screen, clock, "vis.gif")  # Uruchamiamy symulację przez 500 kroków
