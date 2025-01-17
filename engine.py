START_POSITION = [
    ["bR", "bH", "bB", "bQ", "bK", "bB", "bH", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["__", "__", "__", "__", "__", "__", "__", "__"],
    ["__", "__", "__", "__", "__", "__", "__", "__"],
    ["__", "__", "__", "__", "__", "__", "__", "__"],
    ["__", "__", "__", "__", "__", "__", "__", "__"],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wH", "wB", "wQ", "wK", "wB", "wH", "wR"]
]

class Game_state():
    def __init__(self):
        self.board = START_POSITION
        self.white_to_move = True
        self.move_log = []
        self.checkmate = False
        self.stalemate = False
    
    def make_move(self, move):
        start_row, start_col = move[0]
        end_row, end_col = move[1]
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = "__"
        self.board[end_row][end_col] = piece
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move


