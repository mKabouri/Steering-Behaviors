import pygame

import config
from environment import SteeringEnvironment

from behaviors.seek import SeekParticule
from behaviors.flee import FleeParticule
from behaviors.pursuit import PursuitBehavior
from behaviors.circuit import CircuitBehavior
from behaviors.flock import FlockingBehavior

if __name__ == '__main__':
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    environment = SteeringEnvironment(screen, FleeParticule)
    environment.draw_environement()
