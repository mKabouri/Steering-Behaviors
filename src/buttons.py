import pygame
import config

def draw_restart_button(screen, mouse_pos):
    restart_button_rect = pygame.Rect(10, 10, 100, 50)  # x, y, width, height
    if restart_button_rect.collidepoint(mouse_pos):
        button_color = config.HOVER_BUTTON_COLOR  # A lighter or different color
    else:
        button_color = config.RESTART_BUTTON_COLOR
    pygame.draw.rect(screen, button_color, restart_button_rect, border_radius=10)
    # Adding a shadow effect
    shadow_rect = restart_button_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2
    pygame.draw.rect(screen, config.SHADOW_COLOR, shadow_rect, border_radius=10)
    # Custom or different font
    font = pygame.font.SysFont("arial", 24)  # You can use a custom font here
    text = font.render('Restart', True, config.TEXT_COLOR)
    text_rect = text.get_rect(center=restart_button_rect.center)
    # Blit text on top of the button
    screen.blit(text, text_rect)
    return restart_button_rect
