class Piece():
    def __init__(self, value, color, position):
        self.value = value
        self.color = color
        self.position = position
        self.img_str = f'images/{color}_{value}.png'

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__('P', color, position)
        self.direction = -1 if color == 'white' else 1
        if (self.position[0] == 6 and self.color == 'white') or (self.position[0] == 1 and self.color == 'black'):
            self.has_moved = False
        else:
            self.has_moved = True
    
    def get_valid_moves(self, board):
        valid_moves = []
        if self.color == 'white':
            if not self.has_moved:
                if board[self.position[0] - 2][self.position[1]] == "__":
                    start_square = self.position
                    end_square = (self.position[0] + self.direction * 2, self.position[1])
                    valid_moves.append([start_square, end_square])

            if board[self.position[0] - 1][self.position[1]] == "__":
                start_square = self.position
                end_square = (self.position[0] + self.direction, self.position[1])
                valid_moves.append([start_square, end_square])

            if self.position[1] == 0:
                diagonals = [(self.position[0] + self.direction, self.position[1] + 1)]
            elif self.position[1] == 7:
                diagonals = [(self.position[0] + self.direction, self.position[1] - 1)]
            else:
                diagonals = [(self.position[0] + self.direction, self.position[1] - 1), (self.position[0] + self.direction, self.position[1] + 1)]

            for square in diagonals:
                if board[square[0]][square[1]] != "__" and board[square[0]][square[1]][0] == 'b':
                    start_square = self.position
                    end_square = square
                    valid_moves.append([start_square, end_square])
                                
        else:
            if not self.has_moved:
                if board[self.position[0] + 2][self.position[1]] == "__" and not self.has_moved:
                    start_square = self.position
                    end_square = (self.position[0] + self.direction * 2, self.position[1])
                    valid_moves.append([start_square, end_square])
            if board[self.position[0] + 1][self.position[1]] == "__":
                start_square = self.position
                end_square = (self.position[0] + self.direction, self.position[1])
                valid_moves.append([start_square, end_square])

            if self.position[1] == 0:
                diagonals = [(self.position[0] + self.direction, self.position[1] + 1)]
            elif self.position[1] == 7:
                diagonals = [(self.position[0] + self.direction, self.position[1] - 1)]
            else:
                diagonals = [(self.position[0] + self.direction, self.position[1] - 1), (self.position[0] + self.direction, self.position[1] + 1)]

            for square in diagonals:
                if board[square[0]][square[1]] != "__" and board[square[0]][square[1]][0] == 'w':
                    start_square = self.position
                    end_square = square
                    valid_moves.append([start_square, end_square])

        return valid_moves


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__('H', color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        return valid_moves

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__('B', color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        return valid_moves

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__('R', color, position)

    def get_valid_moves(self, board):
        valid_moves = []
        return valid_moves

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__('Q', color, position)

    def get_valid_moves(self, board):
        valid_moves = []
        return valid_moves

class King(Piece):
    def __init__(self, color, position):
        super().__init__('K', color, position)
        self.can_castle_queen_side = True
        self.can_castle_king_side = True
    
    def get_valid_moves(self, board):
        valid_moves = []
        return valid_moves