import pygame

import config
from environment import SteeringEnvironment
from seek import SeekParticule

if __name__ == '__main__':
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    environment = SteeringEnvironment(screen, SeekParticule)
    environment.draw_environement()
