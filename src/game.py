import pygame
import sys
from .settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLUE, WHITE, BLACK,
    MENU, PLAYING, PAUSED, GAME_OVER, LEVEL_COMPLETE,
    FONT, background_image
)
from .sprites import Player, Heart
from .ui import Button, draw_menu, draw_pause_menu, draw_game_over, draw_level_complete
from .level_manager import load_level, get_max_level

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sonchi's Adventure")
    clock = pygame.time.Clock()

    # Initialize game state
    game_state = MENU
    current_level = 1
    max_level = get_max_level()
    player = None
    projectiles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    # Create menu buttons
    menu_buttons = [
        Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2, 200, 50, "Start Game", lambda: setattr(sys.modules[__name__], 'game_state', PLAYING)),
        Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 70, 200, 50, "Quit", pygame.quit)
    ]
    
    pause_buttons = [
        Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 50, 200, 50, "Resume"),
        Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 20, 200, 50, "Quit to Menu")
    ]

    # Load background music
    pygame.mixer.music.load('sounds/background.wav')
    pygame.mixer.music.play(-1)  # Loop indefinitely

    # Load first level
    level_data = load_level(current_level)
    platforms = level_data['platforms']
    enemies = level_data['enemies']
    coins = level_data['coins']
    level_end = level_data['level_end']
    
    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif game_state == MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in menu_buttons:
                        if button.is_clicked(event.pos):
                            if button.text == "Start Game":
                                game_state = PLAYING
                                player = Player(100, 500)
                                all_sprites.add(player)
                            elif button.text == "Quit":
                                running = False
            
            elif game_state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = PAUSED
                    elif event.key == pygame.K_SPACE:
                        if player:
                            player.jump()
                    elif event.key == pygame.K_x:
                        if player:
                            projectile = player.shoot()
                            if projectile:
                                projectiles.add(projectile)
                                all_sprites.add(projectile)
            
            elif game_state == PAUSED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = PLAYING
                for button in pause_buttons:
                    if button.handle_event(event):
                        if button.text == "Resume":
                            game_state = PLAYING
                        elif button.text == "Quit to Menu":
                            game_state = MENU
            
            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Restart the current level
                        level_data = load_level(current_level)
                        platforms = level_data['platforms']
                        enemies = level_data['enemies']
                        coins = level_data['coins']
                        level_end = level_data['level_end']
                        player = Player(100, 500)
                        all_sprites = pygame.sprite.Group()
                        all_sprites.add(player)
                        projectiles = pygame.sprite.Group()
                        game_state = PLAYING
            
            elif game_state == LEVEL_COMPLETE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        current_level += 1
                        if current_level > max_level:
                            game_state = MENU
                        else:
                            level_data = load_level(current_level)
                            platforms = level_data['platforms']
                            enemies = level_data['enemies']
                            coins = level_data['coins']
                            level_end = level_data['level_end']
                            player = Player(100, 500)
                            all_sprites = pygame.sprite.Group()
                            all_sprites.add(player)
                            projectiles = pygame.sprite.Group()
                            game_state = PLAYING

        # Update
        if game_state == PLAYING and player is not None:
            # Update game objects
            player.update(platforms, projectiles, enemies, coins, level_end)
            enemies.update(platforms)
            projectiles.update(enemies)
            
            # Check for level completion
            if level_end and pygame.sprite.collide_rect(player, level_end):
                game_state = LEVEL_COMPLETE
            
            # Check for game over
            if player.lives <= 0:
                game_state = GAME_OVER

        # Draw
        if game_state == MENU:
            draw_menu(screen, menu_buttons)
        elif game_state == PLAYING and player is not None:
            # Draw background with parallax effect
            screen.blit(background_image, (-player.camera_x * 0.5, 0))
            
            # Draw all sprites with camera offset
            for platform in platforms:
                screen.blit(platform.image, (platform.rect.x - player.camera_x, platform.rect.y))
            for projectile in projectiles:
                screen.blit(projectile.image, (projectile.rect.x - player.camera_x, projectile.rect.y))
            for enemy in enemies:
                screen.blit(enemy.image, (enemy.rect.x - player.camera_x, enemy.rect.y))
            for coin in coins:
                screen.blit(coin.image, (coin.rect.x - player.camera_x, coin.rect.y))
            if level_end:
                screen.blit(level_end.image, (level_end.rect.x - player.camera_x, level_end.rect.y))
            
            # Draw player and hearts
            screen.blit(player.image, (player.rect.x - player.camera_x, player.rect.y))
            player.hearts.draw(screen)
            
            # Draw UI elements (these don't move with camera)
            coin_text = FONT.render(f'Coins: {player.coins}', True, WHITE)
            screen.blit(coin_text, (WINDOW_WIDTH - 150, 10))
            
            level_text = FONT.render(f'Level {current_level}', True, WHITE)
            screen.blit(level_text, (WINDOW_WIDTH // 2 - 50, 10))
        elif game_state == PAUSED:
            # Draw game in background
            screen.fill(BLUE)
            draw_pause_menu(screen, pause_buttons)
        elif game_state == GAME_OVER:
            draw_game_over(screen)
        elif game_state == LEVEL_COMPLETE:
            draw_level_complete(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 