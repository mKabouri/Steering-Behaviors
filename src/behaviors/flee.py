import numpy as np
from behaviors.base_particule import Particule
import config

class FleeParticule(Particule):
    def __init__(
            self,
            coordinate,
            velocity,
            acceleration,
            targets
        ):
        super().__init__(coordinate, velocity, acceleration, targets)

    def update_target(self):
        if self.targets:
            self.target_x, self.target_y = min(self.targets, key=lambda t: np.linalg.norm(np.array(t) - np.array((self.x, self.y))))
        else:
            self.target_x, self.target_y = self.x, self.y

    def particule_behavior(self):
        # If the nearest target changes
        self.update_target()

        error = (self.x - self.target_x, self.y - self.target_y)  # Invert direction for fleeing
        distance = np.linalg.norm(error, ord=2)
        
        if distance < config.FLEE_RADIUS:
            if distance > 0:
                desired_velocity = np.array(error) / distance * config.MAX_SPEED
                steer_force = desired_velocity - np.array([self.v_x, self.v_y])

                if np.linalg.norm(steer_force) > config.MAX_FORCE:
                    steer_force = steer_force / np.linalg.norm(steer_force) * config.MAX_FORCE

                # Update acceleration
                self.acc_x, self.acc_y = steer_force

        # Update velocity
        self.v_x += self.acc_x
        self.v_y += self.acc_y

        speed = np.linalg.norm([self.v_x, self.v_y])
        if speed > config.MAX_SPEED:
            self.v_x, self.v_y = self.v_x/speed*config.MAX_SPEED, self.v_y/speed*config.MAX_SPEED

        # Update position
        self.x += self.v_x
        self.y += self.v_y
        # If in boundaries switch direction
        if self.x <= 0 or self.x >= config.WIDTH:
            self.v_x *= -1
            self.x = max(0, min(self.x, config.WIDTH))
        if self.y <= 0 or self.y >= config.HEIGHT:
            self.v_y *= -1
            self.y = max(0, min(self.y, config.HEIGHT))
        return True
