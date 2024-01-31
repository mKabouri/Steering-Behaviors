import pygame
import pygame.gfxdraw
import math
import random
import numpy as np

import config
from buttons import draw_restart_button
from behaviors.seek import SeekParticule
from behaviors.flee import FleeParticule 
from behaviors.circuit import CircuitBehavior
from behaviors.flock import FlockingBehavior

class SteeringEnvironment():
    _cback = (128, 128, 128)
    _cfore = (10, 10, 10)
    _cwidth = 30

    def __init__(self, screen, behavior):
        self.screen = screen
        # Three lists to store targets, particules and obstacles (in case of circuit behavior)
        self.behavior = behavior
        self.targets = []
        self.particules: list[behavior] = []
        self.obstacles = []

        self.circuit_coords = config.CIRCUIT_COORDS
    
    def reset_environment(self):
        self.targets.clear()
        self.particules.clear()
        self.obstacles.clear()

    def update_neighbors(self):
        # This is for flocking behavior
        for particule in self.particules:
            particule.neighbors = [p for p in self.particules if p != particule and np.linalg.norm(np.array([p.x, p.y]) - np.array([particule.x, particule.y])) < config.NEIGHBOR_RADIUS]

    def add_particule(self, coord):
        # Generate a random angle
        if self.behavior == FlockingBehavior:
            velocity = np.random.uniform(-1, 1, 2)
            particule = FlockingBehavior(coord, velocity, (0, 0), None, [])
            self.particules.append(particule)
            return True
        angle = random.uniform(0, 2*math.pi)
        initial_velocity_x = config.INITIAL_VELOCITY[0]*math.cos(angle)
        initial_velocity_y = config.INITIAL_VELOCITY[1]*math.sin(angle)
        new_particule = self.behavior(coord, (initial_velocity_x, initial_velocity_y), config.INITIAL_FORCE, self.targets)        
        print(f"New particule added at position: {(new_particule.x, new_particule.y)} with direction: {(initial_velocity_x, initial_velocity_y)}")
        self.particules.append(new_particule)
        return True

    def add_target(self, coord):
        self.targets.append(coord)
        print(f"New target added at position: {coord}")

    def __draw_targets(self):
        colors = [config.YELLOW, config.GRAY]
        if self.behavior == SeekParticule or self.behavior == FleeParticule:
            for coord in self.targets:
                outer_radius = config.FLEE_RADIUS
                ring_width = 10
                for i in range(5, 0, -1):
                    color_index = i%2
                    pygame.draw.circle(self.screen, colors[color_index], coord, outer_radius-(ring_width*(5-i)), ring_width)
        elif self.behavior == CircuitBehavior:
            for coord in self.targets:
                pygame.draw.circle(self.screen, colors[0], coord, 6, 0)
                pygame.draw.circle(self.screen, colors[1], coord, 6, 1)

    def __draw_circuit(self):
        start_color = pygame.Color(config.YELLOW)
        end_color = pygame.Color(config.MAUVE)
        num_points = len(self.circuit_coords)
        for i in range(num_points):
            p1 = self.circuit_coords[i]
            p2 = self.circuit_coords[(i+1) % num_points]
            lerp = i/num_points
            color = start_color.lerp(end_color, lerp)
            width = int(self._cwidth/2*(1+math.sin(lerp*math.pi)))

            pygame.draw.line(self.screen, color, p1, p2, width)

            shadow_color = (color.r//2, color.g//2, color.b//2)
            pygame.gfxdraw.filled_circle(self.screen, *p1, width+2, shadow_color)
        for p in self.circuit_coords:
            pygame.gfxdraw.filled_circle(self.screen, *p, 10, pygame.Color(255, 255, 0))
            pygame.gfxdraw.aacircle(self.screen, *p, 10, pygame.Color(0, 0, 0))
        pygame.draw.lines(self.screen, self._cfore, True, self.circuit_coords, 2)
    
    def handle_collisions(self):
        for i in range(len(self.particules)):
            for j in range(i + 1, len(self.particules)):
                particule1 = self.particules[i]
                particule2 = self.particules[j]

                dx = particule1.x-particule2.x
                dy = particule1.y-particule2.y
                distance = math.sqrt(dx**2 + dy**2)
                # Check if the distance is less than collision threshold fixed in config.py
                if distance < config.COLLISION_THRESHOLD:
                    overlap = config.COLLISION_THRESHOLD-distance
                    dx /= distance
                    dy /= distance
                    particule1.x += dx*overlap/2
                    particule1.y += dy*overlap/2
                    particule2.x -= dx*overlap/2
                    particule2.y -= dy*overlap/2

    def is_on_circuit(self, coord):
        for i in range(len(self.circuit_coords)):
            point_a = self.circuit_coords[i]
            point_b = self.circuit_coords[(i+1)%len(self.circuit_coords)]
            # Check if 'coord' is near the line segment from point_a to point_b
            if self.is_near_line_segment(coord, point_a, point_b, threshold=config.OBSTACLE_THRESHOLD):
                return True
        return False

    def is_near_line_segment(self, coord, point_a, point_b, threshold):
        # Calculate the nearest point on the line segment to 'coord'
        nearest_point = self.nearest_point_on_line_segment(coord, point_a, point_b)
        # Check if 'coord' is within the 'threshold' distance of the line segment
        distance = math.sqrt((nearest_point[0]-coord[0])**2 + (nearest_point[1]-coord[1])**2)
        return distance <= threshold

    def nearest_point_on_line_segment(self, coord, point_a, point_b):
        # See vector projection formula for details
        a_to_p = (coord[0]-point_a[0], coord[1]-point_a[1])
        a_to_b = (point_b[0]-point_a[0], point_b[1]-point_a[1])
        a_to_b_squared = a_to_b[0]**2 + a_to_b[1]**2
        dot_product = a_to_p[0]*a_to_b[0] + a_to_p[1]*a_to_b[1]
        t = max(0, min(1, dot_product/a_to_b_squared))
        return (point_a[0]+t*a_to_b[0], point_a[1]+t*a_to_b[1])

    def add_obstacle(self, coord):
        if self.is_on_circuit(coord):
            self.obstacles.append(coord)
            print(f"Obstacle added at {coord}")
        else:
            print("Obstacle not on circuit")

    def __draw_obstacles(self):
        for obstacle in self.obstacles:
            outer_radius = config.OBSTACLE_RADIUS
            inner_radius = 10
            pattern_radius = 15
            num_spikes = 6
            spike_length = 10
            obstacle_color = (244, 67, 54)
            pattern_color = (76, 175, 80)
            pygame.draw.circle(self.screen, obstacle_color, obstacle, outer_radius)
            pygame.draw.circle(self.screen, (255, 255, 255), obstacle, inner_radius)
            pygame.draw.circle(self.screen, pattern_color, obstacle, pattern_radius, 1)
            for i in range(num_spikes):
                angle = (2*math.pi/num_spikes)*i
                end_x = obstacle[0]+math.cos(angle)*(outer_radius+spike_length)
                end_y = obstacle[1]+math.sin(angle)*(outer_radius+spike_length)
                pygame.draw.line(self.screen, pattern_color, obstacle, (end_x, end_y), 2)

    def draw_environement(self):
        pygame.init()
        clock = pygame.time.Clock()    

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Exiting")
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("Exiting")
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If left click add particule. If right click to add target.
                    mouse_x, mouse_y = event.pos
                    if event.button == 1:
                        if restart_button_rect.collidepoint(mouse_x, mouse_y):
                            self.reset_environment()
                        else:
                            self.add_particule((mouse_x, mouse_y))
                    elif event.button == 3:  # Right click
                        if self.behavior == FleeParticule or self.behavior == SeekParticule:
                            self.add_target((mouse_x, mouse_y))
                        elif self.behavior == CircuitBehavior:
                            self.add_obstacle((mouse_x, mouse_y))

            self.screen.fill((255, 255, 255))
            mouse_pos = pygame.mouse.get_pos()
            restart_button_rect = draw_restart_button(self.screen, mouse_pos)
            self.__draw_targets()

            # Steering loop
            self.handle_collisions()
            if self.behavior == CircuitBehavior:
                self.__draw_circuit()
            elif self.behavior == FleeParticule or self.behavior == SeekParticule:
                self.__draw_targets()
            self.update_neighbors()
            for particule in self.particules:
                if self.behavior == CircuitBehavior:
                    particule.particule_behavior(self.obstacles)
                elif self.behavior == FlockingBehavior:
                    particule.particule_behavior(self.particules)
                else:
                    particule.particule_behavior()
                particule.draw_particule(self.screen)
            
            self.__draw_obstacles()

            pygame.display.flip()
            clock.tick(config.FPS)

        pygame.quit()
