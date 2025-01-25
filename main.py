import pygame
import pieces   
from engine import Game_state

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

# def show_positions(board):
#     for i in range(BOARD_SIZE):
#         for j in range(BOARD_SIZE):
#             if board[i][j] != "__":
#                 piece = PIECES[board[i][j][1]]("white" if board[i][j][0] == 'w' else "black", (i, j))
#                 print(piece.value, piece.position)

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

def draw_game(screen, gs):
    draw_board(screen)
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
                if not playerClicks and gs.board[row][col] == "__":
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
                        if move in gs.get_all_valid_moves():                    
                            gs.make_move(move)
                            playerClicks = []
                            sqClicked = ()
                        else:
                            playerClicks = []
                            sqClicked = ()
                            continue

                print(playerClicks)

        draw_game(screen, gs)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
