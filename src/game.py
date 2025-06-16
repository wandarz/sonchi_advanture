import pygame
import sys
from .settings import *
from .sprites import Player, Heart
from .ui import Button, draw_menu, draw_pause_menu, draw_game_over, draw_level_complete
from .level_manager import load_level, get_max_level

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sonchi's Adventure")
    clock = pygame.time.Clock()

    # Game state
    game_state = MENU
    current_level = 1
    max_level = get_max_level()
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    hearts = pygame.sprite.Group()
    
    # Create player
    player = None
    
    # Create buttons
    menu_buttons = [
        Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2, 200, 50, "Start Game"),
        Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 70, 200, 50, "Quit")
    ]
    
    pause_buttons = [
        Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 50, 200, 50, "Resume"),
        Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 20, 200, 50, "Quit to Menu")
    ]

    # Load background music
    pygame.mixer.music.load('sounds/background.wav')
    pygame.mixer.music.play(-1)  # Loop indefinitely

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == MENU:
                for button in menu_buttons:
                    if button.handle_event(event):
                        if button.text == "Start Game":
                            game_state = PLAYING
                            current_level = 1
                            level_data = load_level(current_level)
                            if level_data:
                                platforms = level_data['platforms']
                                enemies = level_data['enemies']
                                coins = level_data['coins']
                                level_end = level_data['level_end']
                                player = Player(100, 500)
                                all_sprites = pygame.sprite.Group()
                                all_sprites.add(player)
                                all_sprites.add(platforms)
                                all_sprites.add(enemies)
                                all_sprites.add(coins)
                                if level_end:
                                    all_sprites.add(level_end)
                                # Create hearts
                                hearts = pygame.sprite.Group()
                                for i in range(player.lives):
                                    heart = Heart(30 + i * 40, 30)
                                    hearts.add(heart)
                                all_sprites.add(hearts)
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
                for button in pause_buttons:
                    if button.handle_event(event):
                        if button.text == "Resume":
                            game_state = PLAYING
                        elif button.text == "Quit to Menu":
                            game_state = MENU
            
            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = MENU
            
            elif game_state == LEVEL_COMPLETE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    current_level += 1
                    if current_level > max_level:
                        game_state = MENU
                    else:
                        game_state = PLAYING
                        level_data = load_level(current_level)
                        if level_data:
                            platforms = level_data['platforms']
                            enemies = level_data['enemies']
                            coins = level_data['coins']
                            level_end = level_data['level_end']
                            player = Player(100, 500)
                            all_sprites = pygame.sprite.Group()
                            all_sprites.add(player)
                            all_sprites.add(platforms)
                            all_sprites.add(enemies)
                            all_sprites.add(coins)
                            if level_end:
                                all_sprites.add(level_end)
                            # Create hearts
                            hearts = pygame.sprite.Group()
                            for i in range(player.lives):
                                heart = Heart(30 + i * 40, 30)
                                hearts.add(heart)
                            all_sprites.add(hearts)

        # Update
        if game_state == PLAYING and player is not None:
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
        screen.fill(BLUE)
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        
        if game_state == MENU:
            draw_menu(screen, menu_buttons)
        elif game_state == PLAYING:
            all_sprites.draw(screen)
            # Draw coin counter
            coin_text = FONT.render(f"Coins: {player.coins if player else 0}", True, WHITE)
            screen.blit(coin_text, (WINDOW_WIDTH - 150, 30))
        elif game_state == PAUSED:
            all_sprites.draw(screen)
            draw_pause_menu(screen, pause_buttons)
        elif game_state == GAME_OVER:
            draw_game_over(screen)
        elif game_state == LEVEL_COMPLETE:
            draw_level_complete(screen, current_level)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 