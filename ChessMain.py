import pygame as p
from Chess import ChessEngine

p.init()

WIDTH = HEIGHT = 512
DIMENSION = 8

SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wp", "bN", "bR", "bB", "bQ", "bK", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []

    validMoves = gs.getValidMoves()
    moveMade = False

    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    validMoves = gs.getValidMoves()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("dark green"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    p.draw.circle(screen, p.Color("dark green"), (int((SQ_SIZE*move.endCol)+(SQ_SIZE/2)),
                                                             int((SQ_SIZE*move.endRow)+(SQ_SIZE/2))), int(SQ_SIZE/9))
                    if gs.board[move.endRow][move.endCol][0] != "-":
                        p.draw.circle(screen, p.Color("dark green"), (int((SQ_SIZE * move.endCol) + (SQ_SIZE / 2)),
                                                                 int((SQ_SIZE * move.endRow) + (SQ_SIZE / 2))),
                                                                int(SQ_SIZE / 2), 2)
    if gs.inCheck:
        if gs.whiteToMove:
            p.draw.circle(screen, p.Color("red"), (int((SQ_SIZE * gs.whiteKingLocation[1]) +
                                                (SQ_SIZE / 2)), int((SQ_SIZE * gs.whiteKingLocation[0])
                                                                + (SQ_SIZE / 2))), int(SQ_SIZE / 2), 2)
        else:
            p.draw.circle(screen, p.Color("red"), (int((SQ_SIZE * gs.blackKingLocation[1]) + (SQ_SIZE / 2)),
                                                   int((SQ_SIZE * gs.blackKingLocation[0]) + (SQ_SIZE / 2))),
                                                int(SQ_SIZE / 2), 2)


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color(240, 217, 181), p.Color(181, 136, 99)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]  # light square if r+c is even, dark if odd
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

