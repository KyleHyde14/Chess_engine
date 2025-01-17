class Piece():
    def __init__(self, value, color, position):
        self.value = value
        self.color = color
        self.position = position
        self.img_str = f'images/{color}_{value}.png'

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__('P', color, position)
        self.has_moved = False
        self.direction = 1 if color == 'white' else -1
    
    def get_valid_moves(self):
        valid_moves = []
        if self.has_moved:
            valid_moves.append((self.position[0] + self.direction, self.position[1]))
        else:
            valid_moves.append((self.position[0] + self.direction, self.position[1]))
            valid_moves.append((self.position[0] + 2 * self.direction, self.position[1]))
        return valid_moves


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__('H', color, position)
    
    def get_valid_moves(self):
        pass

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__('B', color, position)
    
    def get_valid_moves(self):
        pass

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__('R', color, position)

    def get_valid_moves(self):
        pass

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__('Q', color, position)

    def get_valid_moves(self):
        pass

class King(Piece):
    def __init__(self, color, position):
        super().__init__('K', color, position)
        self.can_castle_queen_side = True
        self.can_castle_king_side = True
    
    def get_valid_moves(self):
        pass