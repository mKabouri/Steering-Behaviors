import pygame

import config
from environment import SteeringEnvironment

if __name__ == '__main__':
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    environment = SteeringEnvironment(screen, (500, 500))
    environment.draw_environement()
