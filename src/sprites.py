import pygame
import random
from .settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('sonchi.png')
        self.image = pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.jumping = False
        self.double_jump_available = False
        self.facing_right = True
        self.camera_x = 0
        self.lives = MAX_LIVES
        self.hearts = pygame.sprite.Group()
        self.coins = 0
        self.update_hearts()

    def update_hearts(self):
        self.hearts.empty()
        for i in range(self.lives):
            heart = Heart(10 + i * 40, 10)
            self.hearts.add(heart)

    def take_damage(self):
        self.lives -= 1
        self.update_hearts()
        return self.lives <= 0

    def update(self, platforms, projectiles, enemies, coins, level_end):
        # Handle horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True

        # Update camera position
        self.camera_x = max(0, self.rect.centerx - WINDOW_WIDTH // 2)

        # Flip the image based on direction
        if not self.facing_right:
            self.image = pygame.transform.flip(pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)
        else:
            self.image = pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

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

        # Keep player in bounds vertically
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.velocity_y = 0
            self.jumping = False
            self.double_jump_available = True
            on_ground = True

        # Check for collisions with enemies
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if self.take_damage():
                    return True  # Game over

        # Check for coin collection
        for coin in coins:
            if self.rect.colliderect(coin.rect):
                coin.kill()
                self.coins += 1
                pygame.mixer.Sound('sounds/coin.wav').play()

        # Check for level completion
        if level_end and self.rect.colliderect(level_end.rect):
            return "level_complete"

        return False

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

    def shoot(self):
        direction = 1 if self.facing_right else -1
        projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
        pygame.mixer.Sound('sounds/shoot.wav').play()
        return projectile

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('boljanjac.png')
        self.image = pygame.transform.scale(self.original_image, (ENEMY_SIZE, ENEMY_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = random.choice([-1, 1])
        self.speed = ENEMY_SPEED
        self.velocity_y = 0
        self.jumping = False
        self.double_jump_available = False
        self.facing_right = self.direction > 0
        self.change_direction_timer = 0
        self.change_direction_delay = random.randint(60, 180)

    def update(self, platforms):
        # Randomly change direction
        self.change_direction_timer += 1
        if self.change_direction_timer >= self.change_direction_delay:
            self.direction = random.choice([-1, 1])
            self.change_direction_timer = 0
            self.change_direction_delay = random.randint(60, 180)

        # Move horizontally
        self.rect.x += self.speed * self.direction
        self.facing_right = self.direction > 0

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

        # Keep enemy in bounds vertically
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.velocity_y = 0
            self.jumping = False
            self.double_jump_available = True
            on_ground = True

        # Random jumping
        if on_ground and random.random() < 0.02:
            self.jump()

        # Flip the image based on direction
        if not self.facing_right:
            self.image = pygame.transform.flip(pygame.transform.scale(self.original_image, (ENEMY_SIZE, ENEMY_SIZE)), True, False)
        else:
            self.image = pygame.transform.scale(self.original_image, (ENEMY_SIZE, ENEMY_SIZE))

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_FORCE
            self.jumping = True
            self.double_jump_available = True

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = PROJECTILE_SPEED

    def update(self, platforms, enemies):
        self.rect.x += self.speed * self.direction
        # Remove projectile if it goes off screen
        if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH * 3:
            self.kill()
        
        # Check for hits
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.kill()
                self.kill()
                pygame.mixer.Sound('sounds/hit.wav').play()
                break

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
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class LevelEnd(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 