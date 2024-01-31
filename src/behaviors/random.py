import random
import config
from behaviors.base_particule import Particule

class RandomBehavior(Particule):
    def __init__(self, coordinate, velocity, acceleration, targets):
        super().__init__(coordinate, velocity, acceleration, targets)

    def update_target(self):
        return
    
    def particule_behavior(self):
        self.acc_x = random.uniform(-config.MAX_FORCE, config.MAX_FORCE)
        self.acc_y = random.uniform(-config.MAX_FORCE, config.MAX_FORCE)

        self.v_x += self.acc_x
        self.v_y += self.acc_y

        speed = (self.v_x**2+self.v_y**2)**0.5
        if speed > config.MAX_SPEED:
            self.v_x = (self.v_x/speed)*config.MAX_SPEED
            self.v_y = (self.v_y/speed)*config.MAX_SPEED

        self.x += self.v_x
        self.y += self.v_y

        self.x = max(0, min(self.x, config.WIDTH))
        self.y = max(0, min(self.y, config.HEIGHT))
