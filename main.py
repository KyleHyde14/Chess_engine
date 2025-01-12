import pygame

WINDOW_SIZE = 512  
BOARD_SIZE = 8     
CELL_SIZE = WINDOW_SIZE // BOARD_SIZE  

# Colores
WHITE = (222,184,135)
BLACK = (79,48,31)

START_POSITIONS = [
    ["R", "H", "B", "Q", "K", "B", "H", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "H", "B", "Q", "K", "B", "H", "R"]
]

def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_pieces(screen, pieces, position):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = START_POSITIONS[row][col]
            if piece != ' ':
                piece_color = 'white' if row >= 6 else 'black'
                piece_img = pygame.image.load(f'images/{piece_color}_{piece}.png')
                screen.blit(piece_img, (col * CELL_SIZE, row * CELL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Chess Baby")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(screen)
        draw_pieces(screen, 0, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
