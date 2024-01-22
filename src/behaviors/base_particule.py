from abc import ABC, abstractmethod
import pygame
import numpy as np
import random

import config

# When updating an agent's movements, it's important to
# check the agent's new velocity against a maximum velocity
# limit. If the velocity is too big, we set it to the maximum
# velocity so our agent won't move too fast.

class Particule(ABC):
    def __init__(
            self,
            coordinate,
            velocity,
            acceleration,
            targets
        ):
        self.x, self.y = coordinate
        self.v_x, self.v_y = velocity
        self.acc_x, self.acc_y = acceleration
        self.color = random.sample(config.POSSIBLE_COLORS, 1)[0]
        self.targets = targets


    def draw_particule(self, screen):
        # The top of the triangle should be in the direction of the target
        angle = np.arctan2(self.v_y, self.v_x)
        tip = (self.x+15*np.cos(angle), self.y+15*np.sin(angle))
        left = (self.x-8*np.cos(angle-np.pi/2), self.y-8*np.sin(angle-np.pi/2))
        right = (self.x-8*np.cos(angle+np.pi/2), self.y-8*np.sin(angle+np.pi/2))
        triangle_coords = [tip, left, right]

        pygame.draw.polygon(screen, self.color, triangle_coords)
        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], 3)

    @abstractmethod
    def update_target(self):
        """
        Update target
        """
        pass

    @abstractmethod
    def particule_behavior(self):
        pass
