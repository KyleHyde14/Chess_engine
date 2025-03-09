import pygame
import pieces   
from engine import Game_state
from brain import make_random_move, find_best_move_minimax, find_best_move_negamax

WINDOW_SIZE = 512  
BOARD_SIZE = 8     
CELL_SIZE = WINDOW_SIZE // BOARD_SIZE
FPS = 60  

WHITE = (222,184,135)
BLACK = (79,48,31)

IMAGES = {}

PIECES = {
    'P': pieces.Pawn,
    'H': pieces.Knight,
    'B': pieces.Bishop,
    'R': pieces.Rook,
    'Q': pieces.Queen,
    'K': pieces.King
}

def load_images():
    for piece in PIECES:
        for color in ['white', 'black']:
            img = pygame.image.load(f'images/{color}_{piece}.png')
            img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
            current_color = 'w' if color == 'white' else 'b'
            IMAGES[f'{current_color}{piece}'] = img

def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_pieces(screen, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            square = board[row][col]
            if square != "__":
                color = square[0]
                piece = PIECES[square[1]]("white" if color == 'w' else "black", (row, col))
                screen.blit(IMAGES[f'{color}{piece.value}'], (col * CELL_SIZE, row * CELL_SIZE))

def draw_promotion_choices(screen, window_size, color):
    WIDTH, HEIGHT = window_size, window_size
    PADDING = 20  
    PIECE_SIZE = WIDTH // 8
    y_pos = PADDING if color == "b" else HEIGHT - PIECE_SIZE - PADDING  

    options = [f'{color}Q', f'{color}R', f'{color}B', f'{color}H']
    buttons = {}
    start_x = (WIDTH - (PIECE_SIZE * 4 + PADDING * 3)) // 2

    BACKGROUND = (50, 50, 50)

    pygame.draw.rect(screen, BACKGROUND, (0, y_pos - PADDING, WIDTH, PIECE_SIZE + 2 * PADDING))  

    for i, piece in enumerate(options):
        rect = pygame.Rect(start_x + i * (PIECE_SIZE + PADDING), y_pos, PIECE_SIZE, PIECE_SIZE)
        buttons[piece] = rect
        pygame.draw.rect(screen, (170, 170, 170), rect, border_radius=5)
        piece_img = pygame.transform.smoothscale(IMAGES[piece], (PIECE_SIZE, PIECE_SIZE))
        screen.blit(piece_img, rect.topleft)

    pygame.display.flip()
    return buttons  

def get_promotion_choice(screen, window_size, color):
    buttons = draw_promotion_choices(screen, window_size, color)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for piece, rect in buttons.items():
                    x, y = event.pos
                    if rect.collidepoint(x, y):
                        return piece
                return None
                    


def highlight_moves(screen, gs, sqClicked):
    if not sqClicked:
        return
    row, col = sqClicked
    turn = 'w' if gs.white_to_move else 'b'
    if gs.board[row][col][0] == turn:
        surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        surface.set_alpha(150)
        surface.fill((233,215,0))
        screen.blit(surface, (col * CELL_SIZE, row * CELL_SIZE))
        surface.set_alpha(50)
        surface.fill((233,215,0))
        piece = PIECES[gs.board[row][col][1]]("white" if gs.board[row][col][0] == 'w' else "black", (row, col))
        if piece.value == 'K':
            opponent_turn = 'b' if gs.white_to_move else 'w'
            attacked_squares = gs.get_attacked_squares(gs.board, opponent_turn)
            ksc = gs.white_ksc if gs.white_to_move else gs.black_ksc
            qsc = gs.white_qsc if gs.white_to_move else gs.black_qsc
            for move in gs.get_legal_moves(piece.get_castle_moves(gs.board, attacked_squares, ksc, qsc)):
                row, col = move.end_square
                screen.blit(surface, (col * CELL_SIZE, row * CELL_SIZE))
        elif piece.value == 'P':
            en_passant_square = gs.en_passant_square
            en_passant_move = piece.get_en_passant_moves(gs.board, en_passant_square)
            if en_passant_move:
                row, col = en_passant_move.end_square
                screen.blit(surface, (col * CELL_SIZE, row * CELL_SIZE))
        for move in gs.get_legal_moves(piece.get_valid_moves(gs.board)):
            row, col = move.end_square
            screen.blit(surface, (col * CELL_SIZE, row * CELL_SIZE))

def draw_end_message(screen, message):
    width, height = screen.get_size()    
    font = pygame.font.SysFont("Arial", 40, bold=True)
    text_surface = font.render(message, True, (20, 20, 20))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

def draw_game(screen, gs, sqClicked):
    draw_board(screen)
    highlight_moves(screen, gs, sqClicked)
    draw_pieces(screen, gs.board)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    gs = Game_state()
    pygame.display.set_caption("Chess Baby")
    clock = pygame.time.Clock()
    running = True
    load_images()
    sqClicked = ()
    playerClicks = []
    whiteAI = False
    blackAI = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE
                if not playerClicks:
                    if gs.board[row][col] == "__":
                        continue
                    elif gs.white_to_move and gs.board[row][col][0] == 'b' or not gs.white_to_move and gs.board[row][col][0] == 'w':
                        continue
                if sqClicked == (row, col):
                    sqClicked = ()
                    playerClicks = []
                else:
                    sqClicked = (row, col)
                    playerClicks.append(sqClicked)
                if len(playerClicks) == 2:
                    piece = gs.board[playerClicks[0][0]][playerClicks[0][1]]
                    if piece[0] == 'w' and not gs.white_to_move or piece[0] == 'b' and gs.white_to_move:
                        playerClicks = []
                        sqClicked = ()
                        continue
                    else:
                        move = pieces.Move(playerClicks[0], playerClicks[1], gs.board)
                        legal_moves = gs.get_legal_moves(gs.get_all_possible_moves())
                        for i in range(len(legal_moves)):
                            if move == legal_moves[i]:  
                                if move.promotion:
                                    color = 'w' if gs.white_to_move else 'b'
                                    new_piece = get_promotion_choice(screen, WINDOW_SIZE, color)
                                    if new_piece:
                                        gs.make_move(move, new_piece=new_piece)  
                                else:            
                                    gs.make_move(legal_moves[i])
                                    playerClicks = []
                                    sqClicked = ()
                        else:
                            playerClicks = []
                            sqClicked = ()
                            continue
            if (gs.white_to_move and whiteAI) or (not gs.white_to_move and blackAI):
                AImove = find_best_move_negamax(gs, 3)
                gs.make_move(AImove)

        draw_game(screen, gs, sqClicked)
        
        if gs.checkmate() or gs.stalemate():
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if gs.checkmate():
                    winner = 'Black' if gs.white_to_move else 'White'
                    message = f'Checkmate! {winner} wins!'
                else:
                    message = "It's a Draw!!"

                draw_end_message(screen, message)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
