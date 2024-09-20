# --- START OF FILE draw.py ---
import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 1500, 800
PIECE_SIZE = (75, 75)
square_size = 75

# Colors
WHITE = (255, 255, 255)
BLUE = (72, 118, 255)
MidnightBlue = (25, 25, 112)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# Load chess pieces images
wp = pygame.transform.scale(pygame.image.load('img/white_pawn.png'), PIECE_SIZE)
bp = pygame.transform.scale(pygame.image.load('img/black_pawn.png'), PIECE_SIZE)
wn = pygame.transform.scale(pygame.image.load('img/white_knight.png'), PIECE_SIZE)
bn = pygame.transform.scale(pygame.image.load('img/black_knight.png'), PIECE_SIZE)
wb = pygame.transform.scale(pygame.image.load('img/white_bishop.png'), PIECE_SIZE)
bb = pygame.transform.scale(pygame.image.load('img/black_bishop.png'), PIECE_SIZE)
wr = pygame.transform.scale(pygame.image.load('img/white_rook.png'), PIECE_SIZE)
br = pygame.transform.scale(pygame.image.load('img/black_rook.png'), PIECE_SIZE)
wq = pygame.transform.scale(pygame.image.load('img/white_queen.png'), PIECE_SIZE)
bq = pygame.transform.scale(pygame.image.load('img/black_queen.png'), PIECE_SIZE)
wk = pygame.transform.scale(pygame.image.load('img/white_king.png'), PIECE_SIZE)
bk = pygame.transform.scale(pygame.image.load('img/black_king.png'), PIECE_SIZE)
logo = pygame.transform.scale(pygame.image.load('img/logo.png'), (100, 100))
restart = pygame.transform.scale(pygame.image.load('img/restart.png'), (100, 100))
switch = pygame.transform.scale(pygame.image.load('img/switch.png'), (100, 100))

def draw_background(win):
    for x in range(8):
        for y in range(8):
            if (x + y) % 2 == 0:
                color = WHITE
            else:
                color = BLUE
            pygame.draw.rect(win, color, pygame.Rect(x * square_size + 100, y * square_size + 100, square_size, square_size))
    win.blit(logo, (1300, 500))
    win.blit(restart, (800, 500))
    win.blit(switch, (1000, 500))

def draw_pieces(win, fen, human_white):
    def fen_to_array(fen):
        fen = fen.split()[0]
        arr = []
        rows = fen.split('/')
        for row in rows:
            row_arr = []
            for ch in str(row):
                if ch.isdigit():
                    for _ in range(int(ch)):
                        row_arr.append('.')
                else:
                    row_arr.append(ch)
            arr.append(row_arr)
        return arr

    arr = fen_to_array(fen=fen)

    piece_to_variable = {
        'p': bp,
        'n': bn,
        'b': bb,
        'r': br,
        'q': bq,
        'k': bk,
        'P': wp,
        'N': wn,
        'B': wb,
        'R': wr,
        'Q': wq,
        'K': wk,
    }

    if not human_white:
        arr = np.array(arr)
        arr = np.flip(arr, axis=[0, 1])

    for x in range(8):
        for y in range(8):
            if arr[y][x] == '.':
                continue

            piece = piece_to_variable[arr[y][x]]
            win.blit(piece, (x * square_size + 100, y * square_size + 100))  # Offset the pieces to match the board

# --- END OF FILE draw.py ---