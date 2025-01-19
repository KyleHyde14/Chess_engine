import pieces

PIECES = {
    'P': pieces.Pawn,
    'H': pieces.Knight,
    'B': pieces.Bishop,
    'R': pieces.Rook,
    'Q': pieces.Queen,
    'K': pieces.King
}

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

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            start_row, start_col = move[0]
            end_row, end_col = move[1]
            piece = self.board[end_row][end_col]
            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = "__"
            self.white_to_move = not self.white_to_move

    def get_all_valid_moves(self):
        all_valid_moves = []
        for row in range(0, 8):
            for col in range(0, 8):
                square = self.board[row][col]
                if square != '__':
                    piece = PIECES[square[1]]('white' if square[0] == 'w' else 'black', (row, col))
                    all_valid_moves.extend(piece.get_valid_moves(self.board))

        return all_valid_moves


