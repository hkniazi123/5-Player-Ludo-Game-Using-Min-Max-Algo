import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 950, 750
BOARD_SIZE = 400
CENTER = (WIDTH // 2, HEIGHT // 2)
PLAYER_COLORS = [(255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 50), (255, 50, 255)]
TOKEN_RADIUS = 16
DICE_SIZE = 50
SAFE_TILE_COLOR = (220, 220, 220)
POWERUP_TILE_COLOR = (180, 230, 255)
NUM_TILES = 40
MIN_RADIUS = BOARD_SIZE // 2 - 100
MAX_RADIUS = BOARD_SIZE // 2
DOUBLE_ROLL = "double_roll"
SAFE_ZONE = "safe_zone"

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("5-Player Ludo with AI")
font = pygame.font.SysFont('Arial', 18, bold=True)
large_font = pygame.font.SysFont('Arial', 28, bold=True)
small_font = pygame.font.SysFont('Arial', 14)

class Token:
    def __init__(self):
        self.position = -1  # -1: home base, 0-39: on board, 40: reached home

class Player:
    def __init__(self, player_id, color):
        self.id = player_id
        self.color = color
        self.tokens = [Token() for _ in range(3)]
        self.tokens_home = 0
    
    def get_score(self):
        score = self.tokens_home * 10
        for token in self.tokens:
            if token.position >= 0:
                score += (40 - token.position)
        return score

class LudoGame:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.board = self.create_board()
        self.players = [Player(i, PLAYER_COLORS[i]) for i in range(5)]
        self.current_player = 0
        self.dice_roll = 1
        self.game_over = False
        self.winner = None
        self.turn_state = "rolling"
        self.available_moves = []
        self.powerup_effect = None
        pygame.display.flip()
    
    def create_board(self):
        board = []
        for player_id in range(5):
            path = []
            for tile in range(40):
                if tile in [0, 8, 16, 24, 32]:
                    tile_type = SAFE_ZONE
                elif tile in [5, 13, 21, 29, 37]:
                    tile_type = random.choice([DOUBLE_ROLL, SAFE_ZONE])
                else:
                    tile_type = "normal"
                path.append({"type": tile_type, "occupants": []})
            board.append(path)
        return board
    
    def roll_dice(self):
        if self.turn_state != "rolling":
            return False
        self.dice_roll = random.randint(1, 6)
        self.turn_state = "moving"
        self.available_moves = self.get_available_moves(self.current_player)
        if not self.available_moves:
            self.next_player()
            return True
        return True
    
    def get_available_moves(self, player_id):
        moves = []
        player = self.players[player_id]
        for token_id, token in enumerate(player.tokens):
            if token.position == -1:
                if self.dice_roll == 6:
                    moves.append((token_id, "start"))
            elif token.position >= 0:
                new_pos = token.position + self.dice_roll
                if new_pos >= 39:
                    moves.append((token_id, "home"))
                else:
                    moves.append((token_id, "move"))
        return moves
    
    def make_move(self, player_id, token_id, move_type):
        if self.turn_state != "moving":
            return False
        player = self.players[player_id]
        if token_id < 0 or token_id >= len(player.tokens):
            return False
        token = player.tokens[token_id]
        if move_type == "start":
            if token.position != -1 or self.dice_roll != 6:
                return False
            token.position = 0
            self.board[player_id][0]["occupants"].append((player_id, token_id))
        elif move_type == "move":
            if not (0 <= token.position < 40):
                return False
            current_tile = self.board[player_id][token.position]
            if (player_id, token_id) not in current_tile["occupants"]:
                return False
            new_pos = token.position + self.dice_roll
            if new_pos >= 40:
                return False
            current_tile["occupants"].remove((player_id, token_id))
            new_tile = self.board[player_id][new_pos]
            if new_tile["type"] != SAFE_ZONE:
                for opp_player_id, opp_token_id in new_tile["occupants"]:
                    if opp_player_id != player_id:
                        self.players[opp_player_id].tokens[opp_token_id].position = -1
                new_tile["occupants"] = []
            token.position = new_pos
            new_tile["occupants"].append((player_id, token_id))
            if new_tile["type"] in [DOUBLE_ROLL, SAFE_ZONE]:
                self.powerup_effect = new_tile["type"]
                self.turn_state = "powerup"
                return True
        elif move_type == "home":
            if not (0 <= token.position < 40):
                return False
            current_tile = self.board[player_id][token.position]
            if (player_id, token_id) not in current_tile["occupants"]:
                return False
            current_tile["occupants"].remove((player_id, token_id))
            token.position = 40
            player.tokens_home += 1
            if player.tokens_home >= 2:
                self.game_over = True
                self.winner = player_id
                return True
        else:
            return False
        if self.turn_state != "powerup":
            self.next_player()
        return True
    
    def use_powerup(self, player_id):
        if self.turn_state != "powerup":
            return False
        if self.powerup_effect == DOUBLE_ROLL:
            self.turn_state = "rolling"
            self.powerup_effect = None
            return True
        elif self.powerup_effect == SAFE_ZONE:
            self.next_player()
            self.powerup_effect = None
            return True
        return False
    
    def next_player(self):
        self.current_player = (self.current_player + 1) % 5
        self.turn_state = "rolling"
        self.dice_roll = 1
        self.available_moves = []
    
    def get_game_state(self):
        state = {
            "current_player": self.current_player,
            "players": [],
            "board": self.board,
            "dice_roll": self.dice_roll,
            "available_moves": self.available_moves
        }
        for player in self.players:
            player_state = {
                "id": player.id,
                "tokens_home": player.tokens_home,
                "tokens": [token.position for token in player.tokens]
            }
            state["players"].append(player_state)
        return state
    
    def apply_game_state(self, state):
        self.current_player = state["current_player"]
        self.dice_roll = state["dice_roll"]
        self.available_moves = state["available_moves"]
        for player_state in state["players"]:
            player = self.players[player_state["id"]]
            player.tokens_home = player_state["tokens_home"]
            for i, pos in enumerate(player_state["tokens"]):
                player.tokens[i].position = pos
        for path in self.board:
            for tile in path:
                tile["occupants"] = []
        for player in self.players:
            for token_id, token in enumerate(player.tokens):
                if 0 <= token.position < 40:
                    self.board[player.id][token.position]["occupants"].append((player.id, token_id))

class AIPlayer:
    def __init__(self, player_id, depth=2):
        self.player_id = player_id
        self.depth = depth
    
    def get_move(self, game):
        original_state = game.get_game_state()
        best_move = None
        best_value = -math.inf
        for move in original_state["available_moves"]:
            game_copy = LudoGame()
            game_copy.apply_game_state(original_state)
            game_copy.make_move(self.player_id, move[0], move[1])
            value = self.minimax(game_copy, self.depth - 1, -math.inf, math.inf, False)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move
    
    def minimax(self, game, depth, alpha, beta, is_maximizing):
        if depth == 0 or game.game_over:
            return self.evaluate(game)
        current_player_id = game.current_player
        is_current_player = (current_player_id == self.player_id)
        if is_current_player or is_maximizing:
            max_eval = -math.inf
            for move in game.get_available_moves(current_player_id):
                game_copy = LudoGame()
                game_copy.apply_game_state(game.get_game_state())
                game_copy.make_move(current_player_id, move[0], move[1])
                eval = self.minimax(game_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in game.get_available_moves(current_player_id):
                game_copy = LudoGame()
                game_copy.apply_game_state(game.get_game_state())
                game_copy.make_move(current_player_id, move[0], move[1])
                eval = self.minimax(game_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def evaluate(self, game):
        our_score = game.players[self.player_id].get_score()
        opponents_score = sum(p.get_score() for i, p in enumerate(game.players) if i != self.player_id)
        return our_score - (opponents_score / 4)

def get_pentagon_point(center, radius, point_idx):
    angle = 2 * math.pi * point_idx / 5 - math.pi/2
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    return (x, y)

def get_tile_position(player_id, tile_idx):
    player_angle = 2 * math.pi * player_id / 5 - math.pi / 2
    segment_length = 8
    segment = tile_idx // segment_length
    segment_pos = tile_idx % segment_length
    start_angle = player_angle + (2 * math.pi / 5) * segment
    end_angle = player_angle + (2 * math.pi / 5) * (segment + 1)
    t = segment_pos / segment_length
    angle = start_angle * (1 - t) + end_angle * t
    radius = MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS) * abs(t - 0.5) * 2
    x = CENTER[0] + radius * math.cos(angle)
    y = CENTER[1] + radius * math.sin(angle)
    return int(x), int(y)

def get_home_base_position(player_id):
    angle = 2 * math.pi * player_id / 5 - math.pi/2
    x = CENTER[0] + (BOARD_SIZE//2 + 70) * math.cos(angle)
    y = CENTER[1] + (BOARD_SIZE//2 + 70) * math.sin(angle)
    return (int(x), int(y))

def draw_board(game):
    screen.fill((245, 245, 220))  # Cream background for a classic look
    
    # Draw central home area
    pygame.draw.polygon(screen, (255, 255, 255), [get_pentagon_point(CENTER, 60, i) for i in range(5)])
    pygame.draw.polygon(screen, (0, 0, 0), [get_pentagon_point(CENTER, 60, i) for i in range(5)], 3)
    
    # Draw main board
    board_points = [get_pentagon_point(CENTER, BOARD_SIZE//2, i) for i in range(5)]
    pygame.draw.polygon(screen, (150, 150, 150), board_points)
    pygame.draw.polygon(screen, (0, 0, 0), board_points, 3)
    
    # Draw paths and tiles with distinct colors for each player's region
    for player_id in range(5):
        for tile_idx in range(NUM_TILES):
            pos = get_tile_position(player_id, tile_idx)
            tile = game.board[player_id][tile_idx]
            
            # Determine the region based on tile index (each player gets 8 tiles per segment)
            segment = tile_idx // 8
            region_player = (player_id + segment) % 5  # Cycle through players for each 8-tile segment
            region_color = PLAYER_COLORS[region_player]  # Use the base color for the region
            
            if tile["type"] == SAFE_ZONE:
                color = SAFE_TILE_COLOR
                border_color = (100, 100, 100)
                symbol = "S"
            elif tile["type"] == DOUBLE_ROLL:
                color = POWERUP_TILE_COLOR
                border_color = (0, 100, 150)
                symbol = "2X"
            else:
                color = region_color  # Use region-specific color for normal tiles
                border_color = (50, 50, 50)
                symbol = ""
            
            pygame.draw.rect(screen, color, (pos[0]-13, pos[1]-13, 26, 26), border_radius=4)
            pygame.draw.rect(screen, border_color, (pos[0]-13, pos[1]-13, 26, 26), 2, border_radius=4)
            if symbol:
                mark_text = small_font.render(symbol, True, (50, 50, 50))
                screen.blit(mark_text, (pos[0]-mark_text.get_width()//2, pos[1]-mark_text.get_height()//2))
    
    # Draw home bases
    for player_id in range(5):
        home_pos = get_home_base_position(player_id)
        pygame.draw.circle(screen, PLAYER_COLORS[player_id], home_pos, 45)
        pygame.draw.circle(screen, (0, 0, 0), home_pos, 45, 3)
        label = font.render(f"Player {player_id+1}", True, (255, 255, 255))
        screen.blit(label, (home_pos[0]-label.get_width()//2, home_pos[1]-label.get_height()//2))
        player = game.players[player_id]
        for token_idx, token in enumerate(player.tokens):
            if token.position == -1:
                angle = 2 * math.pi * token_idx / len(player.tokens)
                token_x = home_pos[0] + 25 * math.cos(angle)
                token_y = home_pos[1] + 25 * math.sin(angle)
                pygame.draw.circle(screen, (255, 255, 255), (token_x, token_y), TOKEN_RADIUS)
                pygame.draw.circle(screen, PLAYER_COLORS[player_id], (token_x, token_y), TOKEN_RADIUS-3)
    
    # Draw tokens on board
    for player in game.players:
        for token_id, token in enumerate(player.tokens):
            if 0 <= token.position < 40:
                pos = get_tile_position(player.id, token.position)
                pygame.draw.circle(screen, player.color, pos, TOKEN_RADIUS)
                pygame.draw.circle(screen, (255, 255, 255), pos, TOKEN_RADIUS-3, 2)
                num_text = small_font.render(str(token_id+1), True, (255, 255, 255))
                screen.blit(num_text, (pos[0]-num_text.get_width()//2, pos[1]-num_text.get_height()//2))
            elif token.position == 40:
                center_pos = get_pentagon_point(CENTER, 30, player.id)
                pygame.draw.circle(screen, player.color, center_pos, TOKEN_RADIUS+2)
                pygame.draw.circle(screen, (255, 255, 255), center_pos, TOKEN_RADIUS, 2)
    
    # Highlight current player's tokens with a yellow outline
    if not game.game_over:
        player = game.players[game.current_player]
        for token_id, token in enumerate(player.tokens):
            if 0 <= token.position < 40:
                pos = get_tile_position(player.id, token.position)
                pygame.draw.circle(screen, (255, 255, 0), pos, TOKEN_RADIUS+3, 3)
            elif token.position == -1:
                home_pos = get_home_base_position(player.id)
                angle = 2 * math.pi * token_id / len(player.tokens)
                token_x = home_pos[0] + 25 * math.cos(angle)
                token_y = home_pos[1] + 25 * math.sin(angle)
                pygame.draw.circle(screen, (255, 255, 0), (token_x, token_y), TOKEN_RADIUS+3, 3)
    
    # Draw player status panels to the left or right of home bases
    panel_width = 130
    panel_height = 90
    padding = 20
    for player_id in range(5):
        home_pos = get_home_base_position(player_id)
        if player_id == 1:
            panel_x = home_pos[0] + 50
            panel_y = home_pos[1] - panel_height // 2
        else:
            panel_x = home_pos[0] - panel_width - 50
            panel_y = home_pos[1] - panel_height // 2
        pygame.draw.rect(screen, (240, 240, 240), (panel_x, panel_y, panel_width, panel_height), border_radius=8)
        pygame.draw.rect(screen, PLAYER_COLORS[player_id], (panel_x, panel_y, panel_width, panel_height), 2, border_radius=8)
        label = font.render(f"Player {player_id+1}", True, (0, 0, 0))
        screen.blit(label, (panel_x + 10, panel_y + 10))
        player = game.players[player_id]
        status_text = f"Home: {player.tokens_home}/3"
        if any(token.position == -1 for token in player.tokens):
            status_text += "\nIn base: " + ",".join(str(i+1) for i, t in enumerate(player.tokens) if t.position == -1)
        if any(0 <= token.position < 40 for token in player.tokens):
            status_text += "\nOn board: " + ",".join(str(i+1) for i, t in enumerate(player.tokens) if 0 <= t.position < 40)
        status_lines = status_text.split('\n')
        for i, line in enumerate(status_lines):
            line_surface = small_font.render(line, True, (0, 0, 0))
            screen.blit(line_surface, (panel_x + 10, panel_y + 35 + i*18))
    
    # Draw current player indicator
    angle = 2 * math.pi * game.current_player / 5 - math.pi/2
    arrow_x = CENTER[0] + (BOARD_SIZE//2 + 60) * math.cos(angle)
    arrow_y = CENTER[1] + (BOARD_SIZE//2 + 60) * math.sin(angle)
    pygame.draw.polygon(screen, PLAYER_COLORS[game.current_player], 
                       [(arrow_x, arrow_y - 15), (arrow_x + 25, arrow_y), (arrow_x, arrow_y + 15)])
    
    # Draw dice
    dice_x, dice_y = WIDTH - 85, HEIGHT - 85
    pygame.draw.rect(screen, (255, 255, 255), (dice_x - DICE_SIZE//2, dice_y - DICE_SIZE//2, DICE_SIZE, DICE_SIZE), border_radius=5)
    pygame.draw.rect(screen, (0, 0, 0), (dice_x - DICE_SIZE//2, dice_y - DICE_SIZE//2, DICE_SIZE, DICE_SIZE), 2, border_radius=5)
    dot_color = (0, 0, 0)
    if game.dice_roll == 1:
        pygame.draw.circle(screen, dot_color, (dice_x, dice_y), 5)
    elif game.dice_roll == 2:
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y - 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y + 10), 5)
    elif game.dice_roll == 3:
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y - 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x, dice_y), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y + 10), 5)
    elif game.dice_roll == 4:
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y - 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y + 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y - 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y + 10), 5)
    elif game.dice_roll == 5:
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y - 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y + 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y - 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y + 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x, dice_y), 5)
    elif game.dice_roll == 6:
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y - 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y), 5)
        pygame.draw.circle(screen, dot_color, (dice_x - 10, dice_y + 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y - 10), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y), 5)
        pygame.draw.circle(screen, dot_color, (dice_x + 10, dice_y + 10), 5)
    
    # Draw game status
    status_text = f"Player {game.current_player+1}'s Turn"
    if game.turn_state == "rolling":
        status_text += " (Roll Dice)"
    elif game.turn_state == "moving":
        status_text += " (Move Token)"
    elif game.turn_state == "powerup":
        status_text += f" (Use {game.powerup_effect})"
    status_surface = large_font.render(status_text, True, PLAYER_COLORS[game.current_player])
    screen.blit(status_surface, (WIDTH//2 - status_surface.get_width()//2, 20))
    
    # Draw available moves for human player
    if game.current_player == 0 and game.turn_state == "moving" and game.available_moves:
        moves_text = "Moves: " + ", ".join([f"Token {m[0]+1} ({m[1]})" for m in game.available_moves])
        moves_surface = font.render(moves_text, True, (0, 0, 0))
        pygame.draw.rect(screen, (240, 240, 240), (20, HEIGHT - 50, moves_surface.get_width() + 20, 30))
        screen.blit(moves_surface, (30, HEIGHT - 45))
    
    # Draw winning message
    if game.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        win_text = f"Player {game.winner+1} Wins!"
        win_surface = large_font.render(win_text, True, PLAYER_COLORS[game.winner])
        screen.blit(win_surface, (WIDTH//2 - win_surface.get_width()//2, HEIGHT//2 - 30))
        restart_text = "Press R to Restart"
        restart_surface = font.render(restart_text, True, (255, 255, 255))
        screen.blit(restart_surface, (WIDTH//2 - restart_surface.get_width()//2, HEIGHT//2 + 20))

def main():
    game = LudoGame()
    ai_players = [AIPlayer(i) for i in range(1, 5)]
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset_game()
                elif event.key == pygame.K_SPACE and not game.game_over:
                    if game.current_player == 0:
                        if game.turn_state == "rolling":
                            game.roll_dice()
                        elif game.turn_state == "moving" and game.available_moves:
                            game.make_move(0, *game.available_moves[0])
                        elif game.turn_state == "powerup":
                            game.use_powerup(0)
        if not game.game_over and game.current_player > 0:
            if game.turn_state == "rolling":
                game.roll_dice()
            elif game.turn_state == "moving":
                ai_move = ai_players[game.current_player - 1].get_move(game)
                if ai_move:
                    game.make_move(game.current_player, *ai_move)
            elif game.turn_state == "powerup":
                game.use_powerup(game.current_player)
        draw_board(game)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()