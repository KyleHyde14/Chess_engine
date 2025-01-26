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
                    valid_moves.append(Move(start_square, end_square, board))

            if board[self.position[0] - 1][self.position[1]] == "__":
                start_square = self.position
                end_square = (self.position[0] + self.direction, self.position[1])
                valid_moves.append(Move(start_square, end_square, board))
                                
        else:
            if not self.has_moved:
                if board[self.position[0] + 2][self.position[1]] == "__" and not self.has_moved:
                    start_square = self.position
                    end_square = (self.position[0] + self.direction * 2, self.position[1])
                    valid_moves.append(Move(start_square, end_square, board))
            if board[self.position[0] + 1][self.position[1]] == "__":
                start_square = self.position
                end_square = (self.position[0] + self.direction, self.position[1])
                valid_moves.append(Move(start_square, end_square, board))

        diagonals = [(self.position[0] + self.direction, self.position[1] - 1), (self.position[0] + self.direction, self.position[1] + 1)]

        for square in diagonals:
            if 0 <= square[0] < 8 and 0 <= square[1] < 8:
                if board[square[0]][square[1]] != "__" and board[square[0]][square[1]][0] != self.color[0]:
                    start_square = self.position
                    end_square = square
                    valid_moves.append(Move(start_square, end_square, board))

        return valid_moves


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__('H', color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        landing_squares = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        start_square = self.position        
        for square in landing_squares:
            if (0 <= (start_square[0] + square[0]) < 8) and (0 <= (start_square[1] + square[1]) < 8):
                end_square = (start_square[0] + square[0], start_square[1] + square[1])
                if board[end_square[0]][end_square[1]][0] != self.color[0]:
                    valid_moves.append(Move(start_square, end_square, board))
            
        return valid_moves

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__('B', color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
        start_square = self.position
        for d in directions:
            for i in range (1, 8):
                if 0 <= (start_square[0] + i*d[0]) < 8 and 0 <= (start_square[1] + i*d[1]) < 8:
                    end_square = (start_square[0] + i*d[0], start_square[1] + i*d[1])
                    if board[end_square[0]][end_square[1]] == "__":
                        valid_moves.append(Move(start_square, end_square, board))   
                    elif board[end_square[0]][end_square[1]][0] != self.color[0]:
                        valid_moves.append(Move(start_square, end_square, board))
                        break
                    else: 
                        break

        return valid_moves

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__('R', color, position)

    def get_valid_moves(self, board):
        valid_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        start_square = self.position
        for d in directions:
            for i in range (1, 8):
                if 0 <= (start_square[0] + i*d[0]) < 8 and 0 <= (start_square[1] + i*d[1]) < 8:
                    end_square = (start_square[0] + i*d[0], start_square[1] + i*d[1])
                    if board[end_square[0]][end_square[1]] == "__":
                        valid_moves.append(Move(start_square, end_square, board))   
                    elif board[end_square[0]][end_square[1]][0] != self.color[0]:
                        valid_moves.append(Move(start_square, end_square, board))
                        break
                    else: 
                        break

        return valid_moves

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__('Q', color, position)

    def get_valid_moves(self, board):
        valid_moves = []
        ROOK = Rook(self.color, self.position)
        BISHOP = Bishop(self.color, self.position)
        valid_moves.extend(ROOK.get_valid_moves(board))
        valid_moves.extend(BISHOP.get_valid_moves(board))
        return valid_moves

class King(Piece):
    def __init__(self, color, position):
        super().__init__('K', color, position)
        self.can_castle_queen_side = True
        self.can_castle_king_side = True
    
    def get_valid_moves(self, board):
        valid_moves = []
        directions = [(1, 0), (1, -1), (1, 1), (0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
        start_square = self.position
        for d in directions:
            if 0 <= (start_square[0] + d[0]) < 8 and 0 <= (start_square[1] + d[1]) < 8:
                end_square = (start_square[0] + d[0], start_square[1] + d[1])
                if board[end_square[0]][end_square[1]][0] != self.color[0]:
                    valid_moves.append(Move(start_square, end_square, board))

        return valid_moves
    
class Move():
    def __init__(self, start_square, end_square, board):
        self.start_square = start_square
        self.end_square = end_square
        self.piece_moved = board[start_square[0]][start_square[1]]
        self.piece_captured = board[end_square[0]][end_square[1]]
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.start_square == other.start_square and self.end_square == other.end_square
        
        return False


