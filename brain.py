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