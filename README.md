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

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.6+ installed. Install Pygame using pip:
   ```bash
   pip install pygame
   ```

3. **Run the Game**:
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
[Insert video link or embed here, e.g., a YouTube or hosted video showcasing gameplay]
*Note*: A gameplay video will be added to demonstrate the board, player interactions, and AI behavior.

## Project Report
### Introduction
The 5-Player Ludo with AI project aims to create an engaging and strategic version of the classic Ludo game, enhanced with AI opponents and unique gameplay mechanics. The project leverages Pygame for graphics and user interaction and implements an AI using the Minimax algorithm to provide challenging opponents.

### Implementation Details
- **Board Design**: The pentagon-shaped board is divided into five paths, each with 40 tiles. Tiles are colored based on player regions, with special tiles for safe zones and power-ups.
- **Game Logic**: Managed by the `LudoGame` class, which handles dice rolls, token movements, power-up effects, and win conditions.
- **AI**: The `AIPlayer` class uses the Minimax algorithm with alpha-beta pruning to evaluate moves. The evaluation function considers the player's score (based on tokens in the home area and board positions) minus the average opponent score.
- **Graphics**: Pygame is used to render the board, tokens, dice, and status panels. The UI highlights the current player's tokens and displays available moves.

### Challenges and Solutions
- **AI Performance**: The Minimax algorithm was initially slow due to the large game state space. Alpha-beta pruning was implemented to reduce computation time.
- **Board Visualization**: Calculating tile positions on a pentagon board was complex. The `get_tile_position` function uses parametric interpolation to place tiles smoothly along curved paths.
- **Power-Ups**: Balancing power-ups required careful design to ensure they enhanced gameplay without being overpowered. The Double Roll and Safe Zone effects were chosen for simplicity and strategic depth.

### Future Improvements
- **Multiplayer Support**: Add support for multiple human players.
- **AI Tuning**: Experiment with deeper search depths or heuristic improvements for smarter AI.
- **Visual Enhancements**: Add animations for token movements and dice rolls.
- **Sound Effects**: Incorporate audio for dice rolls, token captures, and power-up activations.

### Conclusion
This project successfully delivers a fully functional 5-player Ludo game with AI opponents, combining strategic gameplay with an intuitive interface. The use of Minimax with alpha-beta pruning ensures challenging AI, while the pentagon board and power-ups add a unique twist to the classic game.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Pygame community for the robust game development library.
- Inspiration from classic Ludo and modern board game designs.
