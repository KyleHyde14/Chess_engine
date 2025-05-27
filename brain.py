import random

CHECKMATE = 10000

SCORES = {
    'P': 1,
    'H': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 0
}

PIECE_SQUARE_TABLES = {
    'P': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0.5, 1, 1, -2, -2, 1, 1, 0.5],
        [0.5, -0.5, 1, 2, 2, 1, -0.5, 0.5],
        [0, 0, 0, 2.5, 2.5, 0, 0, 0],
        [0.5, 0.5, 1, 2, 2, 1, 0.5, 0.5],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'H': [
        [-5, -4, -3, -3, -3, -3, -4, -5],
        [-4, -2, 0, 0, 0, 0, -2, -4],
        [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
        [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
        [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
        [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
        [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
        [-5, -4, -3, -3, -3, -3, -4, -5]
    ],
    'B': [
        [-2, -1, -1, -1, -1, -1, -1, -2],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
        [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-1, 1, 1, 1, 1, 1, 1, -1],
        [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
        [-2, -1, -1, -1, -1, -1, -1, -2]
    ],
    'R': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0.5, 1, 1, 1, 1, 1, 1, 0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [0, 0, 0, 0.5, 0.5, 0, 0, 0]
    ],
    'Q': [
        [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
        [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
        [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
        [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
        [-1, 0, 0.5, 0, 0, 0, 0, -1],
        [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
    ],
    'K': [
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-2, -3, -3, -4, -4, -3, -3, -2],
        [-1, -2, -2, -2, -2, -2, -2, -1],
        [2, 2, 0, 0, 0, 0, 2, 2],
        [2, 3, 1, 0, 0, 1, 3, 2]
    ]
}

def evaluate(gs):
    board = gs.board
    score = 0
    score += 100 * count_material(board)
    score += positional_score(board)
    score += king_safety_score(gs)
    score += pawn_structure_score(board)
    score += 0.1 * mobility_score(gs)
    score += 0.2 * center_control_score(board)
    return score if gs.white_to_move else -score

def positional_score(board):
    score = 0
    for row in range(8):
        for col in range(8):
            square = board[row][col]
            if square == '--':
                continue
            color, piece = square[0], square[1]
            pst = PIECE_SQUARE_TABLES.get(piece)
            if pst:
                
                table_bonus = pst[row][col] if color == 'w' else pst[7 - row][col]
                score += table_bonus if color == 'w' else -table_bonus
    return score

def pawn_structure_score(board):
    white_pawns = [[] for _ in range(8)]
    black_pawns = [[] for _ in range(8)]
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == '--':
                continue
            if piece == 'wP':
                white_pawns[col].append(row)
            elif piece == 'bP':
                black_pawns[col].append(row)
    
    for col in range(8):
        if len(white_pawns[col]) > 1:
            score -= 0.5 * (len(white_pawns[col]) - 1)
        if len(black_pawns[col]) > 1:
            score += 0.5 * (len(black_pawns[col]) - 1)
    
    for col in range(8):
        if white_pawns[col]:
            if (col == 0 or not white_pawns[col-1]) and (col == 7 or not white_pawns[col+1]):
                score -= 0.5
        if black_pawns[col]:
            if (col == 0 or not black_pawns[col-1]) and (col == 7 or not black_pawns[col+1]):
                score += 0.5

    for col in range(8):
        for row in white_pawns[col]:
            is_passed = all((not black_pawns[c] or max(black_pawns[c]) > row) for c in range(max(0, col-1), min(7, col+1)+1))
            if is_passed:
                score += 1
        for row in black_pawns[col]:
            is_passed = all((not white_pawns[c] or min(white_pawns[c]) < row) for c in range(max(0, col-1), min(7, col+1)+1))
            if is_passed:
                score -= 1
    return score

def king_safety_score(gs):
    score = 0
    board = gs.board
    for color, sign in [('w', 1), ('b', -1)]:
        king_row, king_col = -1, -1
        for row in range(8):
            for col in range(8):
                if board[row][col] == f'{color}K':
                    king_row, king_col = row, col
        if color == 'w':
            if king_row == 7 and (king_col == 6 or king_col == 2):
                score += 1  
            if king_row < 6:
                score -= 1  
        else:
            if king_row == 0 and (king_col == 6 or king_col == 2):
                score -= 1  
            if king_row > 1:
                score += 1  
    return score

def mobility_score(gs):
    num_moves = len(gs.get_legal_moves(gs.get_all_possible_moves()))
    return num_moves

def center_control_score(board):
    center = [(3, 3), (3, 4), (4, 3), (4, 4)]
    score = 0
    for row, col in center:
        square = board[row][col]
        if square == '--':
            continue
        color = square[0]
        score += 0.5 if color == 'w' else -0.5
    return score

def make_random_move(move_list):
    return random.choice(move_list)

def evaluate(gs):
    return count_material(gs.board)

def minimax_alpha_beta(gs, depth, alpha, beta, maximizing_player, ply=0):
    if gs.checkmate():
        return -CHECKMATE + ply if maximizing_player else CHECKMATE - ply
    if gs.stalemate():
        return 0
    if depth == 0:
        return evaluate(gs)

    valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())

    if maximizing_player:
        max_eval = -float('inf')
        for move in valid_moves:
            gs.make_move(move)
            eval = minimax_alpha_beta(gs, depth-1, alpha, beta, False, ply+1)
            gs.undo_move()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves:
            gs.make_move(move)
            eval = minimax_alpha_beta(gs, depth-1, alpha, beta, True, ply+1)
            gs.undo_move()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
        
    
def find_best_move_minimax(gs, depth):
    best_move = None
    maximizing_player = gs.white_to_move
    alpha = -float('inf')
    beta = float('inf')
    best_score = -float('inf') if maximizing_player else float('inf')

    for move in gs.get_legal_moves(gs.get_all_possible_moves()):
        gs.make_move(move)
        score = minimax_alpha_beta(gs, depth-1, alpha, beta, not maximizing_player, ply=1)
        gs.undo_move()

        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)

    return best_move

def negamax_alpha_beta(gs, depth, alpha, beta, color, ply=0):
    if gs.checkmate():
        return -color * (CHECKMATE - ply)
    elif gs.stalemate():
        return 0
    if depth == 0:
        return color * evaluate(gs)

    best_score = -float('inf')
    valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())

    for move in valid_moves:
        gs.make_move(move)
        score = -negamax_alpha_beta(gs, depth - 1, -beta, -alpha, -color, ply + 1)
        gs.undo_move()

        best_score = max(best_score, score)
        alpha = max(alpha, score)

        if alpha >= beta:
            break

    return best_score

def find_best_move_negamax(gs, depth):
    valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())
    best_move = random.choice(valid_moves)  

    best_score = -float('inf')
    alpha, beta = -float('inf'), float('inf')
    color = 1 if gs.white_to_move else -1

    for move in valid_moves:
        gs.make_move(move)
        score = -negamax_alpha_beta(gs, depth - 1, -beta, -alpha, -color)
        gs.undo_move()

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)

    return best_move

def count_material(board):
        score = 0
        for row in range(8):
            for col in range(8):
                square = board[row][col]
                if square[0] == 'w':
                    score += SCORES[square[1]]
                elif square[0] == 'b':
                    score -= SCORES[square[1]]

        return score