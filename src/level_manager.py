import json
import os
import pygame
from .settings import *
from .sprites import Platform, Enemy, Coin, LevelEnd

def get_max_level():
    """Get the maximum level number from the levels directory"""
    level_files = [f for f in os.listdir('levels') if f.startswith('level') and f.endswith('.json')]
    if not level_files:
        return 0
    return max(int(f.split('level')[1].split('.')[0]) for f in level_files)

def load_level(level_num):
    """Load a level from its JSON file"""
    try:
        with open(f'levels/level{level_num}.json', 'r') as f:
            level_data = json.load(f)
    except FileNotFoundError:
        print(f"Level {level_num} not found!")
        return None

    # Create sprite groups
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    level_end = None
    all_sprites = pygame.sprite.Group()

    # Load platforms
    for platform_data in level_data.get('platforms', []):
        platform = Platform(
            platform_data['x'],
            platform_data['y'],
            platform_data['width'],
            platform_data['height']
        )
        platforms.add(platform)
        all_sprites.add(platform)

    # Load enemies
    if 'enemy_spawns' in level_data:
        for enemy_data in level_data['enemy_spawns']:
            enemy = Enemy(enemy_data['x'], enemy_data['y'], enemy_data['type'])
            enemies.add(enemy)
            all_sprites.add(enemy)

    # Load coins
    for coin_data in level_data.get('coins', []):
        coin = Coin(coin_data['x'], coin_data['y'])
        coins.add(coin)
        all_sprites.add(coin)

    # Load level end position
    if 'end_position' in level_data:
        level_end = LevelEnd(
            level_data['end_position']['x'],
            level_data['end_position']['y']
        )
        all_sprites.add(level_end)

    return {
        'name': level_data.get('name', f'Level {level_num}'),
        'platforms': platforms,
        'enemies': enemies,
        'coins': coins,
        'level_end': level_end,
        'all_sprites': all_sprites
    } 