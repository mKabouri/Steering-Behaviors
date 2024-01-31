import pygame

import config
from environment import SteeringEnvironment

from behaviors.seek import SeekParticule
from behaviors.flee import FleeParticule
from behaviors.circuit import CircuitBehavior
from behaviors.flock import FlockingBehavior
from behaviors.random import RandomBehavior

if __name__ == '__main__':
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    environment = SteeringEnvironment(screen, RandomBehavior)
    environment.draw_environement()
