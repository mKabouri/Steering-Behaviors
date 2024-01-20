import pygame
import numpy as np

import config
from seek import SeekParticule
from buttons import draw_restart_button

class SteeringEnvironment():
    def __init__(self, screen, behavior):
        self.screen = screen
        # Two lists to store targets and particules
        self.behavior = behavior
        self.targets = []
        self.particules: list[SeekParticule] = []
    
    def reset_environment(self):
        self.targets.clear()
        self.particules.clear()

    def add_particule(self, coord):
        new_particule = self.behavior(coord, config.INITIAL_VELOCITY, config.INITIAL_FORCE, self.targets)
        print(f"New particule added at postion: {(new_particule.x, new_particule.y)}")
        self.particules.append(new_particule)
        return True

    def add_target(self, coord):
        self.targets.append(coord)
        print(f"New target added at position: {coord}")

    def __draw_targets(self):
        for coord in self.targets:
            pygame.draw.circle(self.screen, config.YELLOW, coord, 50, 10)

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
            self.__draw_targets()
            for particule in self.particules:
                particule.particule_behavior()
                particule.draw_particule(self.screen)

            pygame.display.flip()
            clock.tick(config.FPS)

        pygame.quit()
