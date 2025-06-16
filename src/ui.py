import pygame
from .settings import *

class Button:
    def __init__(self, x, y, width, height, text, color=MENU_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = FONT
        self.is_hovered = False

    def draw(self, surface):
        color = (min(self.color[0] + 30, 255), 
                min(self.color[1] + 30, 255), 
                min(self.color[2] + 30, 255)) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

def draw_menu(screen, buttons):
    screen.fill(BLUE)
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    
    # Draw title
    title = FONT.render("Sonchi's Adventure", True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)

def draw_pause_menu(screen, buttons):
    # Draw buttons
    for button in buttons:
        button.draw(screen)

def draw_game_over(screen):
    screen.fill(BLACK)
    game_over_text = FONT.render("Game Over", True, RED)
    continue_text = FONT.render("Press ENTER to return to menu", True, WHITE)
    
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(continue_text, continue_rect)

def draw_level_complete(screen, level):
    screen.fill(BLACK)
    complete_text = FONT.render(f"Level {level} Complete!", True, GREEN)
    continue_text = FONT.render("Press ENTER to continue", True, WHITE)
    
    complete_rect = complete_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
    
    screen.blit(complete_text, complete_rect)
    screen.blit(continue_text, continue_rect) 