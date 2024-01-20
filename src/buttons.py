import pygame

import config

def draw_restart_button(screen):
    restart_button_rect = pygame.Rect(10, 10, 100, 50)  # x, y, width, height
    pygame.draw.rect(screen, config.RESTART_BUTTON_COLOR, restart_button_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render('Restart', True, config.TEXT_COLOR)
    text_rect = text.get_rect(center=restart_button_rect.center)
    screen.blit(text, text_rect)
    return restart_button_rect