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

CHECK_POSITION = [
    ['bR', 'bH', 'bB', 'bQ', 'bK', '__', '__', 'bR'],
    ['bP', 'bP', 'bP', '__', '__', 'bP', 'bP', 'bP'], 
    ['__', '__', '__', '__', '__', 'bH', '__', '__'],
    ['__', '__', '__', 'bP', 'wP', '__', '__', '__'], 
    ['__', 'bB', '__', '__', '__', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', 'wH', '__', '__'], 
    ['wP', 'wP', 'wP', '__', 'wP', 'wP', 'wP', 'wP'], 
    ['wR', '__', 'wB', 'wQ', 'wK', 'wB', '__', 'wR']
]

CASTLE_POSITION = [
    ['bR', '__', '__', '__', 'bK', '__', '__', 'bR'],
    ['bP', 'bP', 'bP', '__', '__', 'bP', 'bP', 'bP'], 
    ['__', '__', '__', '__', '__', 'bH', '__', '__'],
    ['__', '__', '__', 'bP', 'wP', '__', '__', '__'], 
    ['__', 'bH', '__', '__', '__', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', 'wH', '__', '__'], 
    ['wP', 'wP', 'wP', '__', 'wP', 'wP', 'wP', 'wP'], 
    ['wR', '__', '__', '__', 'wK', '__', '__', 'wR']
]

# TODO Legal check castling

class Game_state():
    def __init__(self):
        self.board = CASTLE_POSITION
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

        if move.castle:
            if end_col - start_col == 2:
                self.board[end_row][end_col -1] = self.board[end_row][end_col +1]
                self.board[end_row][end_col +1] = "__"
            elif end_col - start_col == - 2:
                self.board[end_row][end_col +1] = self.board[end_row][end_col -2]
                self.board[end_row][end_col -2] = "__"
            
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

            if move.castle:
                if end_col - start_col == 2:
                    self.board[end_row][end_col +1] = self.board[end_row][end_col -1]
                    self.board[end_row][end_col -1] = "__"
                elif end_col - start_col == - 2:
                    self.board[end_row][end_col -2] = self.board[end_row][end_col +1]
                    self.board[end_row][end_col +1] = "__"

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
    
    def get_legal_moves(self, moves):
        legal_moves = []
        for move in moves:
            self.make_move(move)
            king_pos = self.black_king_pos if self.white_to_move else self.white_king_pos
            get_attacked_squares = self.get_attacked_squares(self.board)
            if king_pos not in get_attacked_squares:
                legal_moves.append(move)
            
            self.undo_move()

        return legal_moves 

       

    def get_attacked_squares(self, board):
        turn = 'w' if self.white_to_move else 'b'
        attacked_squares = []
        for row in range(0, 8):
            for col in range(0, 8):
                square = board[row][col]
                if square != '__' and square[0] == turn:
                    piece = PIECES[square[1]]('white' if square[0] == 'w' else 'black', (row, col))
                    attacked_squares.extend(piece.get_attacking_squares(board))

        return attacked_squares



    

