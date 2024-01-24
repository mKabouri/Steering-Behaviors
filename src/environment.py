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

class SteeringEnvironment():
    _cback = (128,128,128)
    _cfore = (10,10,10)
    _cwidth = 30
    def __init__(self, screen, behavior):
        self.screen = screen
        # Two lists to store targets and particules
        self.behavior = behavior
        self.targets = []
        self.particules: list[behavior] = []

        self.circuit_coords = config.CIRCUIT_COORDS
    
    def reset_environment(self):
        self.targets.clear()
        self.particules.clear()

    def add_particule(self, coord):
        # Generate a random angle
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

    def draw_environement(self):
        pygame.init()
        clock = pygame.time.Clock()    

        running = True
        while running:
            self.screen.fill((255, 255, 255))
            restart_button_rect = draw_restart_button(self.screen)
            self.__draw_targets()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("Exiting")
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If left click add particule. If right click to add target.
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if restart_button_rect.collidepoint(mouse_x, mouse_y):
                            self.reset_environment()
                        else:
                            self.add_particule((mouse_x, mouse_y))
                    elif event.button == 3:  # Right click
                        mouse_x, mouse_y = event.pos
                        self.add_target((mouse_x, mouse_y))

            # Steering loop
            if self.behavior == CircuitBehavior:
                self.__draw_circuit()
            elif self.behavior == FleeParticule or self.behavior == SeekParticule:
                self.__draw_targets()
            for particule in self.particules:
                particule.particule_behavior()
                particule.draw_particule(self.screen)

            pygame.display.flip()
            clock.tick(config.FPS)

        pygame.quit()
