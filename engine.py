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
    ['bB', 'bB', '__', '__', '__', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', 'wH', '__', '__'], 
    ['wP', 'wP', 'wP', '__', 'wP', 'wP', 'wP', 'wP'], 
    ['wR', '__', '__', '__', 'wK', '__', '__', 'wR']
]

PROMOTION_POSITION = [
    ['bR', '__', '__', '__', 'bK', '__', '__', 'bR'],
    ['__', 'wP', '__', '__', '__', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', 'wH', '__', '__'], 
    ['__', 'bP', '__', '__', '__', '__', 'bP', '__'], 
    ['wR', '__', '__', '__', 'wK', '__', '__', 'wR']
]

ENPASSANT_POSITION = [
    ['bR', 'bH', 'bB', 'bQ', 'bK', '__', '__', 'bR'],
    ['bP', 'bP', 'bP', '__', '__', 'bP', 'bP', '__'], 
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', 'bP', 'wP', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', '__', '__', 'bP'], 
    ['__', '__', '__', '__', '__', 'wH', '__', '__'], 
    ['wP', 'wP', 'wP', '__', 'wP', 'wP', 'wP', 'wP'], 
    ['wR', '__', 'wB', 'wQ', 'wK', 'wB', '__', 'wR']
]

CHECKMATE_POSITION = [
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', '__', '__', 'bK'],
    ['__', '__', '__', '__', 'bQ', '__', '__', '__'], 
    ['__', '__', '__', '__', 'bQ', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', '__', '__', '__'], 
    ['__', '__', '__', '__', '__', '__', '__', '__'], 
    ['wK', '__', '__', '__', '__', '__', '__', '__']
]

class Game_state():
    def __init__(self):
        self.board = START_POSITION
        self.white_to_move = True
        self.move_log = []
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.white_ksc = True
        self.white_qsc = True
        self.black_ksc = True
        self.black_qsc = True
        self.castle_rights_log = [(True, True, True, True)]
        self.en_passant_square = ()

    
    def make_move(self, move, new_piece=None):
        start_row, start_col = move.start_square
        end_row, end_col = move.end_square
        self.board[start_row][start_col] = "__"
        self.board[end_row][end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wK':
            self.white_king_pos = move.end_square
            self.white_ksc = False
            self.white_qsc = False
        elif move.piece_moved == 'bK': 
            self.black_king_pos = move.end_square
            self.black_ksc = False
            self.black_qsc = False
        elif move.piece_moved == 'wR':
            if move.start_square == (7, 7):
                self.white_ksc = False
            elif move.start_square == (7, 0):
                self.white_qsc = False
        elif move.piece_moved == 'bR':
            if move.start_square == (0, 7):
                self.black_ksc = False
            elif move.start_square == (0, 0):
                self.black_qsc = False
        
        if move.piece_captured == 'wR':
            if move.end_square == (7, 7):
                self.white_ksc = False
            elif move.end_square == (7, 0):
                self.white_qsc = False
        elif move.piece_captured == 'bR':
            if move.end_square == (0, 7):
                self.black_ksc = False
            elif move.end_square == (0, 0):
                self.black_qsc = False

        if move.piece_moved[1] == 'P' and abs(start_row - end_row) == 2:
            self.en_passant_square = ((start_row + end_row)//2, end_col)
        else:
            self.en_passant_square = ()
        
        if move.enPassant:
            self.board[start_row][end_col] = '__'


        if move.castle:
            if end_col - start_col == 2:
                self.board[end_row][end_col -1] = self.board[end_row][end_col +1]
                self.board[end_row][end_col +1] = "__"
            elif end_col - start_col == - 2:
                self.board[end_row][end_col +1] = self.board[end_row][end_col -2]
                self.board[end_row][end_col -2] = "__"
        elif move.promotion:
            if new_piece:
                self.board[end_row][end_col] = new_piece
            else:
                self.board[end_row][end_col] = f'{move.piece_moved[0]}Q'

        self.castle_rights_log.append((self.white_ksc, self.white_qsc,
                                       self.black_ksc, self.black_qsc))
            
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

            if move.piece_moved[1] == 'P' and abs(start_row - end_row) == 2:
                self.en_passant_square = ()
            
            if len(self.move_log) != 0:
                previous_move = self.move_log[-1]
                if previous_move.piece_moved[1] == 'P' and abs(previous_move.end_square[0] - previous_move.start_square[0]) == 2:
                    self.en_passant_square = ((previous_move.end_square[0] + previous_move.start_square[0])//2, previous_move.end_square[1])

            if move.enPassant:
                self.board[end_row][end_col] = '__'
                self.board[start_row][end_col] = move.piece_captured

            if move.castle:
                if end_col - start_col == 2:
                    self.board[end_row][end_col +1] = self.board[end_row][end_col -1]
                    self.board[end_row][end_col -1] = "__"
                elif end_col - start_col == - 2:
                    self.board[end_row][end_col -2] = self.board[end_row][end_col +1]
                    self.board[end_row][end_col +1] = "__"

            self.castle_rights_log.pop()
            self.white_ksc, self.white_qsc, self.black_ksc, self.black_qsc = self.castle_rights_log[-1]

    def get_all_possible_moves(self):
        all_possible_moves = []
        turn = 'w' if self.white_to_move else 'b'
        for row in range(0, 8):
            for col in range(0, 8):
                square = self.board[row][col]
                if square != '__' and square[0] == turn:
                    piece = PIECES[square[1]]('white' if square[0] == 'w' else 'black', (row, col))
                    if piece.value == 'K':
                        opponent_turn = 'b' if self.white_to_move else 'w'
                        attacked_squares = self.get_attacked_squares(self.board, opponent_turn)
                        ksc = self.white_ksc if self.white_to_move else self.black_ksc
                        qsc = self.white_qsc if self.white_to_move else self.black_qsc
                        all_possible_moves.extend(piece.get_castle_moves(self.board, attacked_squares, ksc, qsc))
                    elif piece.value == 'P':
                        en_passant_square = self.en_passant_square
                        if en_passant_square != ():
                            en_passant_move = piece.get_en_passant_moves(self.board, en_passant_square)
                            if en_passant_move:
                                all_possible_moves.append(en_passant_move)
                    all_possible_moves.extend(piece.get_valid_moves(self.board))

        return all_possible_moves
    
    def get_legal_moves(self, moves):
        legal_moves = []
        for move in moves:
            self.make_move(move)
            if not self.in_check(validating=True):
                legal_moves.append(move)
            
            self.undo_move()

        return legal_moves 

       

    def get_attacked_squares(self, board, turn):
        attacked_squares = []
        for row in range(0, 8):
            for col in range(0, 8):
                square = board[row][col]
                if square != '__' and square[0] == turn:
                    piece = PIECES[square[1]]('white' if square[0] == 'w' else 'black', (row, col))
                    attacked_squares.extend(piece.get_attacking_squares(board))

        return attacked_squares
    
    def in_check(self, validating=False):
        if not validating:
            king_pos = self.white_king_pos if self.white_to_move else self.black_king_pos
            turn = 'b' if self.white_to_move else 'w'
            attacked_squares = self.get_attacked_squares(self.board, turn)
        else:
            king_pos = self.black_king_pos if self.white_to_move else self.white_king_pos
            turn = 'w' if self.white_to_move else 'b'
            attacked_squares = self.get_attacked_squares(self.board, turn)
            
        return king_pos in attacked_squares
    
    def checkmate(self):
        valid_moves = self.get_legal_moves(self.get_all_possible_moves())
        return self.in_check() and len(valid_moves) == 0
    
    def stalemate(self):
        valid_moves = self.get_legal_moves(self.get_all_possible_moves())
        return not self.in_check() and len(valid_moves) == 0
       