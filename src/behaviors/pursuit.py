import numpy as np
from behaviors.base_particule import Particule
import config

class PursuitBehavior(Particule):
    def __init__(
            self,
            coordinate,
            velocity,
            acceleration,
            targets
        ):
        super().__init__(coordinate, velocity, acceleration, targets)

    def update_target(self):
        pass

    def particule_behavior(self):
        pass