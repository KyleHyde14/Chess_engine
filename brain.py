import random
from engine import Game_state as gs

def make_random_move(move_list):
    return random.choice(move_list)

def evaluate(gs):
    return gs.count_material()

def minimax(gs, depth, maximize):
    if depth == 0:
        return evaluate(gs)
    elif gs.checkmate():
        return -float('inf') if maximize else float('inf')
    elif gs.stalemate():
        return 0
    
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
        
    
def find_best_move(gs, depth):
    best_move = None
    
    if gs.white_to_move:
        best_score = -float('inf')
        valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())
        for move in valid_moves:
            gs.make_move(move)
            score = minimax(gs, depth - 1, False)
            gs.undo_move()
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('inf')
        valid_moves = gs.get_legal_moves(gs.get_all_possible_moves())
        for move in valid_moves:
            gs.make_move(move)
            score = minimax(gs, depth - 1, True)
            gs.undo_move()
            if score < best_score:
                best_score = score
                best_move = move

    return best_move

