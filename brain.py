import random
from engine import Game_state as gs

SCORES = {
    'P': 1,
    'H': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 0
}

def make_random_move(move_list):
    return random.choice(move_list)

def evaluate(gs):
    return count_material(gs.board)

def minimax(gs, depth, maximize):
    if gs.checkmate():
        return -float('inf') if maximize else float('inf')
    elif gs.stalemate():
        return 0
    if depth == 0:
        return evaluate(gs)
    
    if maximize:
        best_score = -float('inf')
        valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())
        for move in valid_moves:
            gs.make_move(move)
            score = minimax(gs, depth -1, maximize=False)
            gs.undo_move()
            best_score = max(best_score, score)

        return best_score
    else:
        best_score = float('inf')
        valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())
        for move in valid_moves:
            gs.make_move(move)
            score = minimax(gs, depth -1, maximize=True)
            gs.undo_move()
            best_score = min(best_score, score)

        return best_score
        
    
def find_best_move_minimax(gs, depth):
    valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())
    best_move = random.choice(valid_moves)    
    
    if gs.white_to_move:
        best_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move)
            score = minimax(gs, depth - 1, False)
            gs.undo_move()
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('inf')        
        for move in valid_moves:
            gs.make_move(move)
            score = minimax(gs, depth - 1, True)
            gs.undo_move()
            if score < best_score:
                best_score = score
                best_move = move
    
    return best_move

def negamax_alpha_beta(gs, depth, alpha, beta, color):
    if gs.checkmate():
        return -float('inf') * color  
    elif gs.stalemate():
        return 0
    if depth == 0:
        return color * evaluate(gs)

    best_score = -float('inf')
    valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())

    for move in valid_moves:
        gs.make_move(move)
        score = -negamax_alpha_beta(gs, depth - 1, -beta, -alpha, -color)
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