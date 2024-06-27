```markdown
# Game Engine Package - starcrusher2025

## Introduction
This package provides a versatile game engine framework named starcrusher2025. It facilitates the development of 2D games using Pygame by offering essential functionalities such as managing the game window, controlling player entities, handling input, rendering game objects, and more.

## Installation
To install starcrusher2025-games, use pip:

```bash
pip install starcrusher2025-games
```

## Usage
To use starcrusher2025 in your Python projects, follow the examples below:

```python
from starcrusher2025_games import Game
from starcrusher2025_games.configs.menu_config import MenuConfig

# Initialize the game instance
game = Game()

# Set the background color of the game window
game.window.set_bgc(0, 0, 0)  # Sets the background to black
game.window.set_background_image("background.png") # Sets an image for the background

# Set player attributes
game.player.set_color(255, 0, 0)  # Sets the player color to red
game.player.set_start_pos(400, 300)  # Sets the player starting position
game.player.set_size(50, 50)  # Sets the player size
game.player.set_speed(5)  # Sets the player speed
game.player.load_image("player.png")  # Sets an image for the player
game.set_fps(60) # Sets the fps to 60

# Add game objects
obj1 = game.obj(start_pos=(100, 100), size=(50, 50), color=(255, 0, 0), image_path="object_image.png")
obj2 = game.obj(start_pos=(200, 200), size=(75, 75), speed=2, color=(0, 255, 0))

game.add_object(obj1)
game.add_object(obj2)

# Set window size
game.window.set_size(800, 600)  # Sets the game window size

# Customize menu configuration
menu_config = MenuConfig()
menu_config.set_bgc(30, 30, 30)  # Sets the menu background color to dark gray
menu_config.set_bg_image_path("menu_background.png")  # Sets an image for the menu background

# Initialize game menus with custom menu configuration
game.menu = Menu(game.window, menu_config)
game.menu.set_game_instance(game)
game.ingame_menu = InGameMenu(game.window, menu_config)
game.ingame_menu.set_game_instance(game)

# Start the game loop
game.start()
```

## Commands

### `game.window.set_bgc(r, g, b)`
Sets the background color of the game window.

- **Parameters:**
  - `r`: Integer representing the red component of the RGB color (0-255).
  - `g`: Integer representing the green component of the RGB color (0-255).
  - `b`: Integer representing the blue component of the RGB color (0-255).

### `game.player.set_start_pos(start_pos)`
Sets the starting position of the player entity.

- **Parameters:**
  - `start_pos`: Tuple representing the `(x, y)` coordinates of the starting position.

### `game.player.set_size(size)`
Sets the size of the player entity.

- **Parameters:**
  - `size`: Tuple representing the `(width, height)` of the player entity.

### `game.player.set_speed(speed)`
Sets the speed of the player entity.

- **Parameters:**
  - `speed`: Integer value representing the speed of the player.

### `game.player.get_player_position()`
Returns the player position.

### `game.player.load_image(image_path)`
Loads an image file for the player entity.

- **Parameters:**
  - `image_path`: Path to the image file to be loaded for the player.

### `game.window.set_size(width, height)`
Sets the size of the game window.

- **Parameters:**
  - `width`: Width of the game window in pixels.
  - `height`: Height of the game window in pixels.

### `game.set_fps(fps)`
Sets the game's target frames per second (FPS).

- **Parameters:**
  - `fps`: Integer value representing the target frames per second.

### `game.add_object(obj)`
Adds a game object to the game.

- **Parameters:**
  - `obj`: Instance of `GameObject`.

### `game.start()`
Starts the game loop, which handles game logic, rendering, and input handling until the game is stopped or closed.

### `game.stop()`
Stops the game loop and terminates the game.

## Additional Features

### Customizable Menu Configuration (`MenuConfig`)

The `MenuConfig` class allows customization of the menu appearance and behavior.

#### `menu_config.set_bgc(r, g, b)`
Sets the background color of the menus.

- **Parameters:**
  - `r`: Integer representing the red component of the RGB color (0-255).
  - `g`: Integer representing the green component of the RGB color (0-255).
  - `b`: Integer representing the blue component of the RGB color (0-255).

#### `menu_config.set_bg_image_path(image_path)`
Sets the path to the background image used for menus.

- **Parameters:**
  - `image_path`: Path to the image file used as the background for menus.

## Example Scenario

In the example usage, `MenuConfig` is utilized to customize the menu appearance and behavior of the game. By setting background colors and background images for both game menus and in-game menus, developers can create a more engaging user interface for their games.

## License
This project is licensed under the MIT License. See the LICENSE.md file for details.
```

This revised README.md now includes the `MenuConfig` class and demonstrates how it can be used to customize the menu appearance and behavior within the starcrusher2025 game engine framework. Adjust the specifics as needed based on the actual API and capabilities of your game engine.