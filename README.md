Note: All files for this project can be found in the master branch of the repository.

Overview: This is a 2D platformer game developed using Python and the Pygame library. Players navigate through a series of levels filled with obstacles, enemies, and collectibles. The game is designed to provide an engaging platforming experience with smooth character mechanics and interactive gameplay.

Technologies used:
  - Python: For core game logic and structure.
  - Pygame: For graphics rendering, input handling, and game loop management.

Features:
  - 2D Platformer Gameplay: Classic platforming mechanics, including jumping, running, and navigating various obstacles.
  - Character Mechanics: The player can jump and move left or right, with smooth animations and gravity effects.
  - Level Design: Multiple levels designed with increasing difficulty, each with unique layouts and challenges.
  - Interactive Environment:
      - Collectibles: Players can collect coins to increase their score.
      - Enemies: Various enemy types that move and can interact with the player, adding challenge to gameplay.
      - Hazards: Lava and other dangers that players must avoid to prevent losing the game.
  - Dynamic Platforms: Moving platforms that require players to time their jumps and movements.
  - Game States:
      - Main Menu: A user-friendly interface to start the game or exit.
      - Game Over Screen: Displays when the player loses, with options to restart the level or return to the main menu.
      - Victory Screen: Displays when the player completes all levels, celebrating their success.
  - Score Tracking: Real-time score display that updates as players collect coins.
  - Sound Effects: Engaging sound effects for actions such as jumping, collecting items, and game over events.
  - Simple Controls: Easy-to-learn controls suitable for players of all ages, making the game accessible to a wide audience.

Project structure:
  - "platformer.py": The main entry point for the game, containing the game loop, initialization, and event handling. This file coordinates the game’s runtime, managing level progression, game state, and screen updates.
  - "player.py": Defines the Player class, handling player controls, movement, gravity, and collision detection. This file manages the core player mechanics and animations, integrating player inputs and interactions within the game environment.
  - "world.py": Contains the World class, which builds and renders the game world from predefined level data. Responsible for generating the environment, this class loads and places tiles, enemies, platforms, and other level elements.
  - "button.py": Manages the Button class, creating and controlling interactive buttons for the game’s UI (e.g., start, exit, and restart buttons). This file enables user interaction with game menus.
  - "enemy.py": Defines the Enemy class, which handles enemy behavior and movement patterns, as well as interactions with the player, contributing to game challenges.
  - "platform.py": Contains the Platform class, which adds functionality for moving platforms within the game. This class manages platform positions and movement directions to create interactive obstacles.
  - "lava.py": Manages the Lava class, which defines dangerous obstacles that end the game when the player comes into contact. Lava is added to specific levels for increased difficulty.
  - "coin.py": Defines the Coin class, representing collectible items that increase the player’s score when collected. This file handles coin placement and interactions.
  - "exit.py": Contains the Exit class, marking the endpoint for each level. When the player reaches an exit, the game progresses to the next level or displays a victory message.
  - "images/": Directory containing all image assets, including backgrounds, character sprites, tiles, and UI icons.
  - "audio/": Directory containing all audio assets, such as background music and sound effects used throughout the game.

Installation:
  1. Install Pygame library for graphics and game functionalities using pip:  "pip install pygame"
  2. Clone the Repository: "git clone https://github.com/Danamat07/platformer_game.git" then "cd platformer_game"
  3. Run the Game:  "python main.py"

Assets: This project uses images and sounds from the [Platformer Pack Redux](https://kenney.nl/assets/platformer-pack-redux) by [Kenney.nl](https://kenney.nl/). These assets are provided under a public domain license, allowing free use in personal and commercial projects.
