import pygame

# Configuración inicial
WINDOW_SIZE = 600  # Tamaño de la ventana (600x600 píxeles)
BOARD_SIZE = 8     # Tamaño del tablero (8x8)
CELL_SIZE = WINDOW_SIZE // BOARD_SIZE  # Tamaño de cada celda

# Colores
WHITE = (222,184,135)
BLACK = (79,48,31)

def draw_board(screen):
    """Dibuja el tablero de ajedrez en la pantalla."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

def main():
    # Inicializa Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Tablero de Ajedrez")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar tablero
        draw_board(screen)

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
