import pygame
import chess
import chess.engine
from draw import *
from playerv2 import *

MidnightBlue = (25, 25, 125)

# --- Initialize ---
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# --- Chess Engine ---
stockfish_path = "stockfish-windows-x86-64-sse41-popcnt.exe"  # Update with your Stockfish path
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
board = chess.Board()

# --- Game Variables ---
running = True
human_white = True  # Human plays as white initially
selected_square = None
legal_moves = []
engine_depth = 5  # Default engine depth
input_rect = pygame.Rect(900, 400, 200, 50)
active = False
depth_text = str(engine_depth)
font = pygame.font.Font(None, 50)
result_rect = pygame.Rect(800, 200, 200, 50) 


def reset_game():
    """Resets the game to the initial state."""
    global board, selected_square, legal_moves
    board = chess.Board()
    selected_square = None
    legal_moves = []

    if not human_white:
        result = engine.play(board, chess.engine.Limit(depth=engine_depth))
        board.push(result.move)

# --- Main Game Loop ---
import pygame
import chess
import chess.engine
from draw import *
from playerv2 import *

MidnightBlue = (25, 25, 125)

# --- Initialize ---
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# --- Chess Engine ---
stockfish_path = "stockfish-windows-x86-64-sse41-popcnt.exe"  # Update with your Stockfish path
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
board = chess.Board()

# --- Game Variables ---
running = True
human_white = True  # Human plays as white initially
selected_square = None
legal_moves = []
engine_depth = 5  # Default engine depth
input_rect = pygame.Rect(900, 400, 200, 50)
active = False
depth_text = str(engine_depth)
font = pygame.font.Font(None, 50)
result_rect = pygame.Rect(800, 200, 200, 50) 


def reset_game():
    """Resets the game to the initial state."""
    global board, selected_square, legal_moves
    board = chess.Board()
    selected_square = None
    legal_moves = []

    if not human_white:
        result = engine.play(board, chess.engine.Limit(depth=engine_depth))
        board.push(result.move)

# --- Main Game Loop ---
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse click
                x, y = pygame.mouse.get_pos()

                # Check if input box is clicked
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                # Check if restart button is clicked
                if 800 <= x <= 900 and 500 <= y <= 600:
                    reset_game()
                # Check if switch side button is clicked
                elif 1000 <= x <= 1100 and 500 <= y <= 600:
                    human_white = not human_white
                    reset_game()

                else:
                    # Handle piece selection and movement
                    col = (x - 100) // square_size
                    row = (y - 100) // square_size
                    if 0 <= col <= 7 and 0 <= row <= 7:
                        if human_white:
                            square = chess.square(col, 7 - row)
                        else:
                            # Flip the coordinates when the player is black
                            square = chess.square(7 - col, row)
        
                        if selected_square is None:
                            # Select a piece
                            if board.piece_at(square) is not None and board.color_at(square) == human_white:
                                selected_square = square
                                legal_moves = list(board.legal_moves)
                        else:
                            # Move the piece if legal
                            move = chess.Move(selected_square, square)
                            if move in legal_moves:
                                board.push(move)
                                selected_square = None
                                legal_moves = []
        
                                # Engine's turn (if game not over)
                                if not board.is_game_over():
                                    result = engine.play(board, chess.engine.Limit(depth=engine_depth))
                                    board.push(result.move)
                            else:
                                selected_square = None
                                legal_moves = []
             
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    try:
                        engine_depth = int(depth_text)
                        reset_game()
                    except ValueError:
                        print("Invalid depth. Please enter a number.")
                elif event.key == pygame.K_BACKSPACE:
                    depth_text = depth_text[:-1]
                else:
                    depth_text += event.unicode
    

        # --- Drawing ---
    win.fill(MidnightBlue)
    draw_background(win)
    draw_pieces(win, board.fen(), human_white)

    # Highlight selected square and legal moves
    if selected_square is not None:
        # Flip the coordinates if the player is black
        if human_white:
            selected_col = selected_square % 8
            selected_row = 7 - selected_square // 8
        else:
            selected_col = 7 - (selected_square % 8)
            selected_row = selected_square // 8

        # Highlight the selected square
        pygame.draw.rect(win, (255, 0, 0), (
            selected_col * square_size + 100, selected_row * square_size + 100,
            square_size, square_size), 2)

        # Highlight the legal moves
        for move in legal_moves:
            if move.from_square == selected_square:
                if human_white:
                    x = move.to_square % 8
                    y = 7 - move.to_square // 8
                else:
                    x = 7 - (move.to_square % 8)
                    y = move.to_square // 8

                pygame.draw.circle(win, (255, 0, 0), (
                    x * square_size + 100 + square_size // 2, y * square_size + 100 + square_size // 2),
                                   square_size // 4)

    # Render the depth input box
    depth_label = font.render("Depth:", True, (255, 255, 255))
    win.blit(depth_label, (input_rect.x - 130, input_rect.y + 5))  # Adjust the position as needed

    # Render the depth input box
    txt_surface = font.render(depth_text, True, (255, 255, 255))
    input_rect.w = max(100, txt_surface.get_width() + 10)
    win.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
    pygame.draw.rect(win, (255, 255, 255), input_rect, 2)

    if board.is_game_over():
        # Get the result of the game
        result = board.result()

        if result == "1-0":
            result_text = "White Wins!" if human_white else "Engine Wins!"
        elif result == "0-1":
            result_text = "Engine Wins!" if human_white else "White Wins!"
        else:
            result_text = "Draw!"

        # Render result box
        pygame.draw.rect(win, (0, 0, 0), result_rect)  # Background for the result text
        result_surface = font.render(result_text, True, (255, 255, 255))  # Render result text
        win.blit(result_surface, (result_rect.x + 10, result_rect.y + 10))

        # Optionally, display a "Restart" prompt
        restart_text = "Click to Restart"
        restart_surface = font.render(restart_text, True, (255, 255, 255))
        win.blit(restart_surface, (result_rect.x, result_rect.y + 60))

        # Check for click to restart
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 800 <= x <= 1000 and 200 <= y <= 300:
                reset_game()
                running = True  # Allow game loop to continue

    pygame.display.update()
    clock.tick(60)

# --- Quit ---
engine.quit()
pygame.quit()
