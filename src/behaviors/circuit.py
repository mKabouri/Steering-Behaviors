import numpy as np
from behaviors.base_particule import Particule
import config

class CircuitBehavior(Particule):
    _circuit_coords = config.CIRCUIT_COORDS
    def __init__(self, coordinate, velocity, acceleration, targets, max_speed=8, max_force=10):
        super().__init__(coordinate, velocity, acceleration, targets)
        self.moving_to_circuit = True
        self.closest_point, self.closest_segment_index = self._find_closest_point_and_segment()
        self.target = self.closest_point
        
        self.MAX_SPEED = max_speed
        self.MAX_FORCE = max_force

    def update_target(self):
        """
        Update target to the next point on the circuit.
        """
        if np.linalg.norm(np.array((self.x, self.y)) - np.array(self.target)) < config.POINT_REACHED_THRESHOLD:
            self.closest_segment_index = (self.closest_segment_index+1)%len(self._circuit_coords)
            self.target = self._circuit_coords[self.closest_segment_index]

    def distance_point_to_segment(self, p, a, b):
        p, a, b = np.array(p), np.array(a), np.array(b)
        # Get the vector of circuit segment ab
        line_vec = b-a
        line_mag = np.linalg.norm(line_vec)
        if line_mag < 1e-10:
            return np.linalg.norm(p-a), a
        u = np.dot(p-a, line_vec)/line_mag**2
        u = max(0, min(u, 1))
        intersect = a + u*line_vec
        distance = np.linalg.norm(p-intersect)
        return distance, intersect

    def _find_closest_point_and_segment(self):
        min_distance = np.inf
        closest_point = None
        closest_segment_index = 0
        for i in range(len(self._circuit_coords)):
            point_a = self._circuit_coords[i]
            # Don't have out of bounds
            point_b = self._circuit_coords[(i+1)%len(self._circuit_coords)]
            distance, closest_point_on_segment = self.distance_point_to_segment((self.x, self.y), point_a, point_b)
            if distance < min_distance:
                min_distance = distance
                closest_point = closest_point_on_segment
                closest_segment_index = i

        return closest_point, closest_segment_index

    def particule_behavior(self, obstacles):
        self.update_target()
        avoidance_force = self.calculate_avoidance_force(obstacles)
        desired_velocity = np.subtract(self.target, (self.x, self.y))
        desired_velocity = desired_velocity/np.linalg.norm(desired_velocity, ord=2)*self.MAX_SPEED
        steering = np.subtract(desired_velocity, (self.v_x, self.v_y))
        steering = np.clip(steering, -self.MAX_FORCE, self.MAX_FORCE)

        # Apply avoidance force
        steering += avoidance_force

        self.acc_x, self.acc_y = steering
        self.v_x += self.acc_x
        self.v_y += self.acc_y
        self.v_x, self.v_y = self.__limit_velocity(self.v_x, self.v_y)
        self.x += self.v_x
        self.y += self.v_y

    def calculate_avoidance_force(self, obstacles):
        avoidance_force = np.array([0.0, 0.0])
        for obstacle in obstacles:
            obstacle_pos = np.array(obstacle)
            particule_pos = np.array([self.x, self.y])
            distance = np.linalg.norm(particule_pos - obstacle_pos)
            if distance < config.OBSTACLE_AVOIDANCE_RADIUS:
                away_vector = particule_pos - obstacle_pos
                away_vector /= distance  # Normalize
                avoidance_force += away_vector
        return avoidance_force * config.AVOIDANCE_STRENGTH

    def __limit_velocity(self, vx, vy):
        speed = np.sqrt(vx**2+vy**2)
        if speed > self.MAX_SPEED:
            vx = (vx/speed)*self.MAX_SPEED
            vy = (vy/speed)*self.MAX_SPEED
        return vx, vy
