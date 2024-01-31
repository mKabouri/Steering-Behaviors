import argparse
import pygame

import config
from environment import SteeringEnvironment

from behaviors.seek import SeekParticule
from behaviors.flee import FleeParticule
from behaviors.circuit import CircuitBehavior
from behaviors.flock import FlockingBehavior
from behaviors.random import RandomBehavior

def main(behavior_name):
    behaviors = {
        "seek": SeekParticule,
        "flee": FleeParticule,
        "circuit": CircuitBehavior,
        "flock": FlockingBehavior,
        "random": RandomBehavior
    }

    if behavior_name not in behaviors:
        raise ValueError(f"Behavior '{behavior_name}' is not recognized. Valid options are: {list(behaviors.keys())}")

    behavior = behaviors[behavior_name]
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    environment = SteeringEnvironment(screen, behavior)
    environment.draw_environement()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run steering behavior simulations.")
    parser.add_argument('-b', '--behavior', default='circuit', type=str, help='Type of behavior to simulate (seek, flee, circuit, flock, random). Default is circuit.')
    args = parser.parse_args()

    main(args.behavior)
