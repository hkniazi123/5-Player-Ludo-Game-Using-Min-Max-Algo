# 5-Player-Ludo-Game-Using-Min-Max-Algo
## Project Overview
This is a Python-based implementation of a 5-player Ludo game with an AI component, built using the Pygame library. The game features a pentagon-shaped board, unique power-up tiles (Double Roll and Safe Zone), and an AI that uses the Minimax algorithm with alpha-beta pruning for strategic gameplay. The game supports one human player (Player 1) and four AI-controlled players (Players 2–5).

### Features
- **5-Player Gameplay**: Supports up to 5 players, with one human and four AI opponents.
- **Pentagon Board Design**: A visually appealing pentagon-shaped board with distinct player paths.
- **Power-Ups**: Includes "Double Roll" (grants an extra turn) and "Safe Zone" (protects tokens from capture) tiles.
- **AI Opponents**: AI players use the Minimax algorithm with alpha-beta pruning for decision-making.
- **Interactive UI**: Displays player status, available moves, dice rolls, and game state using Pygame.

## Installation
To run the game, you need Python and Pygame installed. Follow these steps:

 **Install Dependencies**:
   Ensure you have Python 3.6+ installed. Install Pygame using pip:
   ```bash
   pip install pygame
   ```
 **Run the Game**:
   Execute the main script to start the game:
   ```bash
   python ludo_game.py
   ```

## Gameplay Instructions
- **Objective**: Move all three of your tokens from the home base to the central home area (pentagon center).
- **Controls**:
  - **Spacebar**: Roll the dice, make a move, or use a power-up (for the human player, Player 1).
  - **R Key**: Restart the game after a win.
- **Rules**:
  - Each player has three tokens, starting in their home base.
  - A roll of 6 allows a token to move from the home base to the starting tile.
  - Tokens move clockwise along the board based on the dice roll.
  - Landing on an opponent's token on a non-safe tile sends the opponent's token back to their home base.
  - Power-up tiles:
    - **Double Roll**: Grants an extra turn.
    - **Safe Zone**: Protects tokens from being captured.
  - The first player to move at least two tokens to the central home area wins.

## Video Demonstration
[https://drive.google.com/file/d/1typ1pZDHYyRfreTSfZdbkwDHbCht9dKF/view?usp=drive_link]


