import pygame
from .settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLUE, WHITE, BLACK,
    FONT
)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = (100, 100, 100)  # Default gray color
        self.hover_color = (150, 150, 150)  # Lighter gray for hover
        self.text_color = WHITE
        self.font = FONT

    def draw(self, surface):
        # Draw button background
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)  # White border
        
        # Draw button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_menu(screen, buttons):
    # Draw background
    screen.fill(BLUE)
    
    # Draw title
    title = FONT.render("Sonchi's Adventure", True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)

def draw_pause_menu(screen):
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Draw pause text
    pause_text = FONT.render("PAUSED", True, WHITE)
    pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    screen.blit(pause_text, pause_rect)
    
    # Draw continue text
    continue_text = FONT.render("Press ESC to continue", True, WHITE)
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
    screen.blit(continue_text, continue_rect)

def draw_game_over(screen):
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Draw game over text
    game_over_text = FONT.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    screen.blit(game_over_text, game_over_rect)
    
    # Draw restart text
    restart_text = FONT.render("Press ENTER to restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
    screen.blit(restart_text, restart_rect)

def draw_level_complete(screen):
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Draw level complete text
    complete_text = FONT.render("LEVEL COMPLETE!", True, WHITE)
    complete_rect = complete_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    screen.blit(complete_text, complete_rect)
    
    # Draw continue text
    continue_text = FONT.render("Press ENTER to continue", True, WHITE)
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
    screen.blit(continue_text, continue_rect) 