import pygame

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (135, 206, 235)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
MENU_BLUE = (0, 100, 255)

# Player properties
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 120
PLAYER_SPEED = 5
JUMP_FORCE = -15
DOUBLE_JUMP_FORCE = -12
GRAVITY = 0.8
MAX_LIVES = 3

# Projectile properties
PROJECTILE_SPEED = 10
PROJECTILE_SIZE = 10

# Enemy properties
ENEMY_SPEED = 2
ENEMY_SIZE = 80

# Coin properties
COIN_SIZE = 30

# Game states
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
LEVEL_COMPLETE = 4

# Initialize font
FONT = pygame.font.Font(None, 36)

# Load background image
background_image = pygame.image.load('images/background.png')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH * 3, WINDOW_HEIGHT)) 