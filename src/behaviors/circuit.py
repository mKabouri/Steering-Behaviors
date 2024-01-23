import numpy as np
from behaviors.base_particule import Particule
import config

class CircuitBehavior(Particule):
    _circuit_coords = config.CIRCUIT_COORDS

    def __init__(self, coordinate, velocity, acceleration, targets):
        super().__init__(coordinate, velocity, acceleration, targets)
        self.current_segment_index = self._find_closest_segment_index()
        self._move_to_closest_point_on_circuit()

    def update_target(self):
        """
        We don't care about the target here. We don't have one.
        """
        return

    def distance_point_to_segment(self, p, a, b):
        p, a, b = np.array(p), np.array(a), np.array(b)
        # Calculate the distance from point p to line segment defined by points a and b
        line_vec = b - a
        line_mag = np.linalg.norm(line_vec)

        if line_mag < 1e-10:
            return np.linalg.norm(p - a)

        u = np.dot(p - a, line_vec)/line_mag**2
        u = max(0, min(u, 1))

        intersect = a + u*line_vec
        return np.linalg.norm(p - intersect)

    def _find_closest_segment_index(self):
        min_distance = np.inf
        closest_segment_index = 0

        for i in range(len(self._circuit_coords)):
            point_a = self._circuit_coords[i]
            point_b = self._circuit_coords[(i + 1) % len(self._circuit_coords)]

            distance = self.distance_point_to_segment((self.x, self.y), point_a, point_b)
            if distance < min_distance:
                min_distance = distance
                closest_segment_index = i

        return closest_segment_index

    def _move_to_closest_point_on_circuit(self):
        point_a = self._circuit_coords[self.current_segment_index]
        point_b = self._circuit_coords[(self.current_segment_index + 1) % len(self._circuit_coords)]

        line_vec = np.array(point_b) - np.array(point_a)
        line_mag = np.linalg.norm(line_vec)

        u = np.dot((self.x, self.y) - np.array(point_a), line_vec) / line_mag**2
        u = max(0, min(u, 1))

        closest_point = np.array(point_a) + u * line_vec
        self.x, self.y = closest_point

    def follow_circuit(self):
        target_point = self._circuit_coords[(self.current_segment_index + 1) % len(self._circuit_coords)]

        desired_velocity = np.subtract(target_point, (self.x, self.y))
        desired_velocity = desired_velocity / np.linalg.norm(desired_velocity) * config.MAX_SPEED
        steering = np.subtract(desired_velocity, (self.v_x, self.v_y))

        if np.linalg.norm(steering) > config.MAX_FORCE:
            steering = steering / np.linalg.norm(steering) * config.MAX_FORCE
        return steering

    def particule_behavior(self):
        # Update the current segment index if the particule reaches the next point
        next_point = self._circuit_coords[(self.current_segment_index + 1) % len(self._circuit_coords)]
        if np.linalg.norm(np.array((self.x, self.y)) - np.array(next_point)) < config.POINT_REACHED_THRESHOLD:
            self.current_segment_index = (self.current_segment_index + 1) % len(self._circuit_coords)

        steering = self.follow_circuit()

        self.v_x, self.v_y = np.add((self.v_x, self.v_y), steering)
        if np.linalg.norm((self.v_x, self.v_y)) > config.MAX_SPEED:
            self.v_x, self.v_y = (self.v_x, self.v_y) / np.linalg.norm((self.v_x, self.v_y)) * config.MAX_SPEED

        self.x += self.v_x
        self.y += self.v_y
