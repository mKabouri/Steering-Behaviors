import pygame
import numpy as np

import config
from seek import SeekParticule

class SteeringEnvironment():
    def __init__(self, screen, target_coord):
        self.screen = screen
        self.target_coord = target_coord
        self.particules: list[SeekParticule] = []
    
    def add_particule(self, coord):
        new_particule = SeekParticule(coord, config.INITIAL_VELOCITY, config.INITIAL_FORCE, self.target_coord)
        print(f"New particule added at postion: {(new_particule.x, new_particule.y)}")
        self.particules.append(new_particule)
        return True

    def __draw_target(self, coord):
        pygame.draw.circle(self.screen, config.YELLOW, coord, 50, 10)

    def draw_environement(self):
        pygame.init()
        clock = pygame.time.Clock()    

        # Add one target and one particule
        self.add_particule((np.random.choice(config.WIDTH), np.random.choice(config.HEIGHT)))

        running = True
        while running:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("Exiting")
                        running = False
            
            # Steering loop
            self.__draw_target(self.target_coord)
            for particule in self.particules:
                particule.particule_behavior()
                particule.draw_particule(self.screen)

            pygame.display.flip()
            clock.tick(config.FPS)

        pygame.quit()
