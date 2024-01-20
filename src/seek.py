import numpy as np
from particule import Particule
import config

class SeekParticule(Particule):
    def __init__(
            self,
            coordinate,
            velocity,
            acceleration,
            target_coord
        ):
        super().__init__(coordinate, velocity, acceleration)
        self.target_x = target_coord[0]
        self.target_y = target_coord[1]

    def particule_behavior(self):
        error = (self.target_x-self.x, self.target_y-self.y)
        distance = np.linalg.norm(error, ord=2)
        if distance < 0.5:
            return True
        if distance > 0:
            error = error/distance
            error = error*config.MAX_SPEED
            steer_force = error-(self.v_x, self.v_y)

            # Test if this force exceeds max_force in config.py
            steer_norm = np.linalg.norm(steer_force, ord=2)
            if steer_norm > config.MAX_FORCE:
                steer_force = (steer_force/steer_norm)*config.MAX_FORCE
            
            # Update acceleration (I assume mass=1 and we have m*acceleration = Force 
            # (second low of newton) then a = F)
            self.acc_x, self.acc_y = steer_force

        # Update velocity (time_step=1)
        self.v_x += self.acc_x
        self.v_y += self.acc_y

        new_speed = np.linalg.norm((self.v_x, self.v_y), ord=2)
        if new_speed > config.MAX_SPEED:
            self.v_x = (self.v_x/new_speed)*config.MAX_SPEED
            self.v_y = (self.v_y/new_speed)*config.MAX_SPEED

        # Update postion        
        self.x += self.v_x
        self.y += self.v_y
        return True