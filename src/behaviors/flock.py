import numpy as np
import random
import config
from behaviors.base_particule import Particule

class FlockingBehavior(Particule):
    def __init__(self, coordinate, velocity, acceleration, targets, neighbors, max_speed=20, max_force=5):
        super().__init__(coordinate, velocity, acceleration, targets)
        self.neighbors = neighbors
        # For random speed at the beginning in the case of flocks
        angle = random.uniform(0, 2*np.pi)
        speed = random.uniform(10, 18)
        self.v_x = np.cos(angle)*speed
        self.v_y = np.sin(angle)*speed

        self.MAX_SPEED = max_speed
        self.MAX_FORCE = max_force

    def update_target(self):
        """
        We don't need it here
        """
        return

    def separation(self):
        """
        Move away from close neighbors of the same color
        """
        steer = np.array([0.0, 0.0])
        total = 0
        for neighbor in self.neighbors:
            if neighbor.color == self.color:
                diff = np.array([self.x-neighbor.x, self.y-neighbor.y])
                dist = np.linalg.norm(diff)
                if dist < config.SEPARATION_DISTANCE:
                    steer += diff/(dist if dist != 0 else 1)
                    total += 1
        if total > 0:
            steer /= total
            steer = (steer/np.linalg.norm(steer))*self.MAX_SPEED-np.array([self.v_x, self.v_y])
            steer = np.clip(steer, -self.MAX_FORCE, self.MAX_FORCE)
        return steer

    def alignment(self):
        """
        Align velocity with neighbors of the same color
        """
        steer = np.array([0.0, 0.0])

        avg_velocity = np.array([0.0, 0.0])
        total = 0
        for neighbor in self.neighbors:
            if neighbor.color == self.color:
                avg_velocity += np.array([neighbor.v_x, neighbor.v_y])
                total += 1
        if total > 0:
            avg_velocity /= total
            if np.linalg.norm(avg_velocity) > 0:
                desired_velocity = (avg_velocity/np.linalg.norm(avg_velocity))*self.MAX_SPEED
                steer = desired_velocity - np.array([self.v_x, self.v_y])
                if np.linalg.norm(steer) > 0:
                    steer = (steer/np.linalg.norm(steer))*self.MAX_SPEED
            steer = np.clip(steer, -self.MAX_FORCE, self.MAX_FORCE)
        return steer

    def cohesion(self):
        """
        Move towards the average position of neighbors of the same color
        """
        center_of_mass = np.array([0.0, 0.0])
        total = 0
        for neighbor in self.neighbors:
            if neighbor.color == self.color:
                center_of_mass += np.array([neighbor.x, neighbor.y])
                total += 1
        if total > 0:
            center_of_mass /= total
            desired_velocity = (center_of_mass-np.array([self.x, self.y]))
            if np.linalg.norm(desired_velocity) > 0:
                desired_velocity = (desired_velocity/np.linalg.norm(desired_velocity))*self.MAX_SPEED
                steer = desired_velocity-np.array([self.v_x, self.v_y])
                steer = np.clip(steer, -self.MAX_FORCE, self.MAX_FORCE)
            return steer
        return np.array([0.0, 0.0])

    def particule_behavior(self):
        sep = self.separation()
        ali = self.alignment()
        coh = self.cohesion()

        # Apply the behaviors
        self.acc_x, self.acc_y = 1.2*sep + 2*ali + coh

        # Update velocity and position as usual
        self.v_x += self.acc_x
        self.v_y += self.acc_y
        self.v_x, self.v_y = self.__limit_velocity(self.v_x, self.v_y)
        self.x += self.v_x
        self.y += self.v_y

        self.__handle_boundaries()
        self.__avoid_boundaries()

    def __limit_velocity(self, vx, vy):
        speed = np.linalg.norm([vx, vy])
        if speed > self.MAX_SPEED:
            vx, vy = (vx/speed)*self.MAX_SPEED, (vy/speed)*self.MAX_SPEED
        return vx, vy

    def __avoid_boundaries(self):
        margin = 5
        steer = np.array([0.0, 0.0])

        if self.x < margin:
            steer[0] += self.MAX_SPEED
        elif self.x > config.WIDTH - margin:
            steer[0] -= self.MAX_SPEED

        if self.y < margin:
            steer[1] += self.MAX_SPEED
        elif self.y > config.HEIGHT-margin:
            steer[1] -= self.MAX_SPEED
        return steer

    def __handle_boundaries(self):
        if self.x <= 0 or self.x >= config.WIDTH or self.y <= 0 or self.y >= config.HEIGHT:
            self.v_x = random.uniform(-self.MAX_SPEED, self.MAX_SPEED)
            self.v_y = random.uniform(-self.MAX_SPEED, self.MAX_SPEED)
            self.x = max(0, min(self.x, config.WIDTH))
            self.y = max(0, min(self.y, config.HEIGHT))
