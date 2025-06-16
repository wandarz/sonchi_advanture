import pygame
import random
from .settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('images/sonchi.png')
        self.image = pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.jumping = False
        self.double_jump_available = False
        self.facing_right = True
        self.lives = MAX_LIVES
        self.coins = 0
        self.camera_x = 0
        self.hearts = pygame.sprite.Group()
        self.update_hearts()
        self.invincible = False
        self.invincible_timer = 0

    def update(self, platforms, projectiles, enemies, coins, level_end):
        # Handle movement
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True

        # Apply velocity
        self.rect.x += self.velocity_x
        
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check for collisions with platforms
        on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.jumping = False
                    self.double_jump_available = True
                    on_ground = True
                elif self.velocity_y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        # Keep player in bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH * 3:  # Limit to level width
            self.rect.right = WINDOW_WIDTH * 3

        # Update camera position
        self.camera_x = max(0, min(self.rect.centerx - WINDOW_WIDTH // 2, WINDOW_WIDTH * 3 - WINDOW_WIDTH))

        # Handle invincibility
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Check for collisions with enemies
        if not self.invincible:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    self.take_damage()
                    self.invincible = True
                    self.invincible_timer = 60  # 1 second of invincibility
                    break

        # Check for collisions with coins
        for coin in coins:
            if self.rect.colliderect(coin.rect):
                coin.kill()
                self.coins += 1
                pygame.mixer.Sound('sounds/coin.wav').play()

        # Flip the image based on direction
        if not self.facing_right:
            self.image = pygame.transform.flip(pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)
        else:
            self.image = pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

    def shoot(self):
        """Create a new projectile"""
        if not self.facing_right:
            projectile = Projectile(self.rect.centerx - 20, self.rect.centery, -1)
        else:
            projectile = Projectile(self.rect.centerx + 20, self.rect.centery, 1)
        return projectile

    def update_hearts(self):
        self.hearts.empty()
        for i in range(self.lives):
            heart = Heart(30 + i * 40, 30)
            self.hearts.add(heart)

    def take_damage(self):
        self.lives -= 1
        self.update_hearts()
        return self.lives <= 0

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_FORCE
            self.jumping = True
            self.double_jump_available = True
            pygame.mixer.Sound('sounds/jump.wav').play()
        elif self.double_jump_available:
            self.velocity_y = DOUBLE_JUMP_FORCE
            self.double_jump_available = False
            pygame.mixer.Sound('sounds/jump.wav').play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='basic'):
        super().__init__()
        self.original_image = pygame.image.load('images/boljanjac.png')
        self.image = pygame.transform.scale(self.original_image, (ENEMY_SIZE, ENEMY_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED
        self.direction = 1
        self.enemy_type = enemy_type
        self.facing_right = True
        self.start_x = x  # Store initial position
        self.patrol_distance = 300  # How far the enemy will patrol from start position

    def update(self, platforms):
        # Move horizontally
        self.rect.x += self.speed * self.direction
        
        # Check patrol boundaries
        if self.rect.x < self.start_x - self.patrol_distance:
            self.direction = 1
            self.facing_right = True
        elif self.rect.x > self.start_x + self.patrol_distance:
            self.direction = -1
            self.facing_right = False
        
        # Check for platform edges
        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                on_platform = True
                # Check if at edge
                if self.direction > 0 and self.rect.right >= platform.rect.right:
                    self.direction = -1
                    self.facing_right = False
                elif self.direction < 0 and self.rect.left <= platform.rect.left:
                    self.direction = 1
                    self.facing_right = True
                break
        
        # Flip the image based on direction
        if not self.facing_right:
            self.image = pygame.transform.flip(pygame.transform.scale(self.original_image, (ENEMY_SIZE, ENEMY_SIZE)), True, False)
        else:
            self.image = pygame.transform.scale(self.original_image, (ENEMY_SIZE, ENEMY_SIZE))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = PROJECTILE_SPEED

    def update(self, enemies):
        # Move projectile
        self.rect.x += self.speed * self.direction
        
        # Check for collisions with enemies
        hits = pygame.sprite.spritecollide(self, enemies, True)
        if hits:
            self.kill()
            return
        
        # Remove if off screen
        if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH:
            self.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/coin.png')
        self.image = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class LevelEnd(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/flag.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/heart.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 