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
pygame.display.set_caption("Checkers")
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


def getPixelPos(i, j):
    return ((j + 0.5) * TILE_SIZE, (i + 0.5) * TILE_SIZE)


def drawBoard(screen):
    for i in range(ROWS):
        for j in range(COLS):
            color = LIGHT_TILE_COLOR if (i + j) % 2 else DARK_TILE_COLOR
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            pygame.draw.rect(screen, color, rect)


def drawPawns(screen):
    for i in range(ROWS):
        for j in range(COLS):
            pawn = (i, j)
            if pawn == chosenPawn:
                continue

            x, y = getPixelPos(i, j)
            color = LIGHT_PAWN_COLOR if board[i][j] == 1 else DARK_PAWN_COLOR

            if board[i][j] != 0:
                pygame.draw.circle(
                    screen,
                    color,
                    (
                        x,
                        y,
                    ),
                    PAWN_SIZE // 2,
                )


def getPawn(mouseX, mouseY):
    for i in range(ROWS):
        for j in range(COLS):
            pawn = board[i][j]
            if pawn == 0:
                continue
            x, y = getPixelPos(i, j)
            dx = x - mouseX
            dy = y - mouseY

            if dx**2 + dy**2 <= (PAWN_SIZE // 2) ** 2:
                return (i, j)

    return None


def movePawn(pawn, mouseX, mouseY):
    if not pawn:
        return
    i, j = pawn
    color = LIGHT_PAWN_COLOR if board[i][j] == 1 else DARK_PAWN_COLOR

    pygame.draw.circle(
        screen,
        color,
        (mouseX, mouseY),
        PAWN_SIZE // 2,
    )

def dropPawn(pawn, mouseX, mouseY):
    if not pawn:
        return

    cellX, cellY = mouseX // TILE_SIZE, mouseY // TILE_SIZE
    i, j = pawn

    prev = board[i][j]
    validMove = False
    delta = 1 if turn else -1
    
    capture = False
    midX, midY = (i + cellY) // 2, (j + cellX) // 2
    
    if cellY - i == delta and abs(cellX - j) == 1:
        validMove = True
    elif cellY - i == delta * 2 and abs(cellX - j) == 2 and board[i][j] * board[midX][midY] == -1:
        capture = True
        validMove = True
    
    if board[cellY][cellX] == 0 and validMove:
        if capture:
            board[midX][midY] = 0
        board[i][j] = 0
        board[cellY][cellX] = prev

        return True

    return False


running = True
turn = False
chosenPawn = None  # (i, j)

while running:
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            res = getPawn(mouseX, mouseY)
            if res:
                i, j = res
                value = board[i][j]
                if (not turn and value == 1) or (turn and value == -1):
                    chosenPawn = res

        if event.type == pygame.MOUSEBUTTONUP:
            res = dropPawn(chosenPawn, mouseX, mouseY)
            if res:
                turn = not turn
            chosenPawn = None

    drawBoard(screen)
    drawPawns(screen)
    movePawn(chosenPawn, mouseX, mouseY)
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()
