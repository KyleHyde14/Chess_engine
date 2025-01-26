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

TEST_POSITION = [
                ['bR', 'bH', 'bB', 'bQ', 'bK', '__', '__', 'bR'],
                ['bP', 'bP', 'bP', '__', '__', 'bP', 'bP', 'bP'], 
                ['__', '__', '__', '__', '__', 'bH', '__', '__'],
                ['__', '__', '__', 'bP', 'wP', '__', '__', '__'], 
                ['__', 'bB', '__', '__', '__', '__', '__', '__'], 
                ['__', '__', '__', '__', '__', 'wH', '__', '__'], 
                ['wP', 'wP', 'wP', '__', 'wP', 'wP', 'wP', 'wP'], 
                ['wR', '__', 'wB', 'wQ', 'wK', 'wB', '__', 'wR']
                ]

class Game_state():
    def __init__(self):
        self.board = START_POSITION
        self.white_to_move = True
        self.move_log = []
        self.checkmate = False
        self.stalemate = False
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
    
    def make_move(self, move):
        start_row, start_col = move.start_square
        end_row, end_col = move.end_square
        self.board[start_row][start_col] = "__"
        self.board[end_row][end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wK':
            self.white_king_pos = move.end_square
        elif move.piece_moved == 'bK': 
            self.black_king_pos = move.end_square
        if move.piece_captured == 'wK':
            self.white_king_pos = None
        elif move.piece_captured == 'bK':
            self.black_king_pos = None

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            start_row, start_col = move.start_square
            end_row, end_col = move.end_square
            self.board[start_row][start_col] = move.piece_moved
            self.board[end_row][end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wK':
                self.white_king_pos = move.start_square
            elif move.piece_moved == 'bK':
                self.black_king_pos = move.start_square

    def get_all_possible_moves(self):
        all_possible_moves = []
        turn = 'w' if self.white_to_move else 'b'
        for row in range(0, 8):
            for col in range(0, 8):
                square = self.board[row][col]
                if square != '__' and square[0] == turn:
                    piece = PIECES[square[1]]('white' if square[0] == 'w' else 'black', (row, col))
                    all_possible_moves.extend(piece.get_valid_moves(self.board))

        return all_possible_moves
    
    def get_legal_moves(self):
        legal_moves = []
        for move in self.get_all_possible_moves():
            self.make_move(move)
            opponent_moves = self.get_all_possible_moves()
            opponent_king_pos = self.black_king_pos if self.white_to_move else self.white_king_pos
            if opponent_king_pos not in [m.end_square for m in opponent_moves]:
                legal_moves.append(move)
            self.undo_move()

        return legal_moves        


    

