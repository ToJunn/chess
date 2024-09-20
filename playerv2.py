import chess

def get_square_from_mouse(x, y, human_white):
    """Converts mouse coordinates to a chessboard square."""
    col = (x - 100) // 75  # Assuming square_size is 75
    row = (y - 100) // 75
    if 0 <= col <= 7 and 0 <= row <= 7:
        if human_white:
            return chess.square(col, 7 - row)
        else:
            return chess.square(7 - col, row)
    return None