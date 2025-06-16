# Sonchi's Adventure

A 2D platformer game built with Pygame where you control Sonchi through various levels, collecting coins and avoiding enemies.

## Features

- Multiple levels with increasing difficulty
- Coin collection system
- Enemy AI with movement and jumping
- Double jump mechanics
- Shooting mechanics
- Lives system
- Background music and sound effects

## Controls

- LEFT/RIGHT arrows: Move
- SPACE: Jump (press again for double jump)
- X: Shoot
- ESC: Pause game

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sonchi_adventure.git
cd sonchi_adventure
```

2. Install the required packages:
```bash
pip install pygame
```

3. Run the game:
```bash
python main.py
```

## Project Structure

```
sonchi_adventure/
├── src/
│   ├── __init__.py
│   ├── game.py
│   ├── settings.py
│   ├── sprites.py
│   ├── ui.py
│   └── level_manager.py
├── levels/
│   ├── level1.json
│   ├── level2.json
│   ├── level3.json
│   ├── level4.json
│   └── level5.json
├── sounds/
│   ├── background.wav
│   ├── jump.wav
│   ├── shoot.wav
│   ├── coin.wav
│   └── hit.wav
├── main.py
├── README.md
└── .gitignore
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 