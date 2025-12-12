import pygame
import sys

pygame.init()

TILE_SIZE = 70
PAWN_SIZE = 40
ROWS, COLS = 8, 8

LIGHT_TILE_COLOR = (240, 220, 130)
DARK_TILE_COLOR = (34, 139, 34)

DARK_PAWN_COLOR = (139, 0, 0)
LIGHT_PAWN_COLOR = (255, 255, 255)

SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Checkers Capture Demo")
clock = pygame.time.Clock()
FPS = 60

board = [
    [0, -1, 0, -1, 0, -1, 0, -1],
    [-1, 0, -1, 0, -1, 0, -1, 0],
    [0, -1, 0, -1, 0, -1, 0, -1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
]


def drawBoard(screen):
    for i in range(ROWS):
        for j in range(COLS):
            color = LIGHT_TILE_COLOR if (i + j) % 2 else DARK_TILE_COLOR
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            pygame.draw.rect(screen, color, rect)


def drawPawns(screen):
    for i in range(ROWS):
        for j in range(COLS):
            pawn = board[i][j]
            color = LIGHT_PAWN_COLOR if pawn == 1 else DARK_PAWN_COLOR
            if pawn != 0:
                pygame.draw.circle(
                    screen,
                    color,
                    ((j + 0.5) * TILE_SIZE, (i + 0.5) * TILE_SIZE),
                    PAWN_SIZE // 2,
                )


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drawBoard(screen)
    drawPawns(screen)
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()
