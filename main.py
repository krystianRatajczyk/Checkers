import pygame
import sys

pygame.init()

TILE_SIZE = 80
PAWN_SIZE = 60
ROWS, COLS = 8, 8

LIGHT_TILE_COLOR = (200, 200, 200)
DARK_TILE_COLOR = (100, 100, 100)

DARK_PAWN_COLOR = (0, 0, 0)
LIGHT_PAWN_COLOR = (255, 255, 255)
DARK_KING_COLOR = (0, 0, 0)
LIGHT_KING_COLOR = (255, 255, 255)

COLORS = {
    1: LIGHT_PAWN_COLOR,
    -1: DARK_PAWN_COLOR,
    2: LIGHT_KING_COLOR,
    -2: DARK_KING_COLOR,
}

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

            if board[i][j] != 0:
                color = COLORS[board[i][j]]
                pygame.draw.circle(
                    screen,
                    color,
                    (
                        x,
                        y,
                    ),
                    PAWN_SIZE // 2,
                )
                if abs(board[i][j]) == 2:  # King Indicator
                    pygame.draw.circle(screen, (255, 215, 0), (x, y), PAWN_SIZE // 4)


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
    color = COLORS[board[i][j]]

    pygame.draw.circle(
        screen,
        color,
        (mouseX, mouseY),
        PAWN_SIZE // 2,
    )
    if abs(board[i][j]) == 2:  # King Indicator
        pygame.draw.circle(screen, (255, 215, 0), (mouseX, mouseY), PAWN_SIZE // 4)


def inBound(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def getMoves(i, j):
    isKing = abs(board[i][j]) == 2  # king is either -2 or 2
    kingMoves = [[1, 1], [-1, -1], [1, -1], [-1, 1]]
    pawnMoves = [[-1, -1], [-1, 1]] if not turn else [[1, 1], [1, -1]]  # going up
    moves = kingMoves if isKing else pawnMoves

    captureMoves = []
    availableMoves = [(i + dx, j + dy) for dx, dy in moves]

    for dx, dy in moves:
        jumpX, jumpY = i + dx, j + dy
        landX, landY = (
            i + dx + dx,
            j + dy + dy,
        )

        if (
            inBound(jumpX, jumpY)
            and inBound(landX, landY)
            and board[jumpX][jumpY] * board[i][j] < 0
            and board[landX][landY] == 0
        ):
            captureMoves.append((landX, landY))

    return (availableMoves, captureMoves)


def mustCapture(turn):
    player = 1 if not turn else -1

    for i in range(ROWS):
        for j in range(COLS):
            pawn = board[i][j]
            if pawn * player > 0:
                _, captureMoves = getMoves(i, j)
                if len(captureMoves) > 0:
                    return True
    return False


def dropPawn(pawn, mouseX, mouseY, turn):
    if not pawn:
        return [False, False]

    col, row = mouseX // TILE_SIZE, mouseY // TILE_SIZE

    i, j = pawn
    hasToCapture = mustCapture(turn)

    availableMoves, captureMoves = getMoves(i, j)

    prev = board[i][j]
    validMove = False
    capture = False

    if (row, col) in availableMoves:
        validMove = True

    if (row, col) in captureMoves:
        validMove = True
        capture = True

    if hasToCapture and not capture:
        validMove = False

    if validMove:
        if capture:  # opposite pawns
            midX, midY = (i + row) // 2, (j + col) // 2
            board[midX][midY] = 0

        board[i][j] = 0
        side = 1 if not turn else -1

        if (not turn and row == 0) or (turn and row == ROWS - 1):
            board[row][col] = 2 * side
        else:
            board[row][col] = prev

    return [validMove, capture]


running = True
turn = False
chosenPawn = None  # (i, j)
forcedPawn = None

while running:
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            res = getPawn(mouseX, mouseY)
            if not res:  # multiple jumps
                continue

            i, j = res
            value = board[i][j]

            # enforce user to select the same pawn during multi-jump
            if forcedPawn is not None and res != forcedPawn:
                chosenPawn = None
                continue

            if (not turn and value > 0) or (
                turn and value < 0
            ):  # check if it correct player due to turn
                if forcedPawn is None and mustCapture(turn):
                    _, captureMoves = getMoves(i, j)

                    if len(captureMoves) == 0:  # selected piece with no beats available
                        chosenPawn = None
                        continue
                chosenPawn = res

        if event.type == pygame.MOUSEBUTTONUP:
            if chosenPawn is None:
                continue

            res, hasCaptured = dropPawn(chosenPawn, mouseX, mouseY, turn)

            if res:
                row, col = mouseY // TILE_SIZE, mouseX // TILE_SIZE

                if hasCaptured:
                    _, captureMoves = getMoves(row, col)

                    if len(captureMoves) > 0:
                        forcedPawn = (row, col)
                    else:
                        turn = not turn
                        forcedPawn = None
                else:
                    turn = not turn
                    forcedPawn = None

            chosenPawn = None

    drawBoard(screen)
    drawPawns(screen)
    movePawn(chosenPawn, mouseX, mouseY)
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()
