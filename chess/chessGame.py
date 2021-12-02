"""
This class is the main class responsible for running the game, setting the game to start, visualize output
and receive input from program.
"""
import numpy as np
import pygame as p
import chessEngine as chs

p.init()  # initialize pygame
'''
initialize board sizes and square size
'''
board_height = board_width = 400
square_size = 400 // 8
images = dict()
MAX_FPS = 15

"""
Loading Images
every piece load a related image from chess/Images/*
"""


def loadImages(images):
    pieces = ["wp", "bp", "wr", "br", "wk", "bk", "wb", "bb", "wq", "bq", "wK", "bK"]  # all posiib, pieces
    for i, piece in enumerate(pieces):  ### for each piece load his related image
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"),
                                          (square_size, square_size))


"""
def main will deal user input and update screen
"""


def main():
    """
    initialize 400x400 screen size and time
    """
    screen = p.display.set_mode((board_height, board_width))
    time = p.time.Clock()
    screen.fill(p.Color('white'))

    """ open a new chess engine from chessBoard && reloading pieces png"""
    engine = chs.chessBoard()
    loadImages(images)

    """ getting all valid moves """
    validMoves = engine.getValidMoves()
    moveMade = False

    """ tracking game driver """
    running = True  # boolean obj. game state end or not
    square_selected = tuple()  # will save the wanted square to be move in each play turn
    curr_move = []  # will save the all play move, from square.... to square
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # if pygame is ended running turn false
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:  # clicking on mouse event
                col, row = p.mouse.get_pos()  # saving the mouse row and col
                row = row // square_size  # resizing it to fit screen
                col = col // square_size

                if square_selected == (row, col):  # if clicked the same square
                    square_selected = tuple()
                    curr_move = []
                else:
                    square_selected = (row, col)  # saving mouse click sata
                    curr_move.append(square_selected)
                    if len(curr_move) == 1 and engine.board[row][col] == "---":
                        square_selected = tuple()
                        curr_move = []
                    elif len(curr_move) == 2:  # if its the 2-nd move
                        move = chs.Move(curr_move[0], curr_move[1], engine.board)
                        if move in validMoves:
                            print(move.getChessNotation())
                            engine.makeMove(move)
                            moveMade = True
                        square_selected = tuple()
                        curr_move = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    engine.undoMove()
                    moveMade = True
                    square_selected = tuple()
                    curr_move = []
            if moveMade:
                moveMade = False
                validMoves = engine.getValidMoves()
        drawGameState(engine.board, screen)
        time.tick(MAX_FPS)
        p.display.flip()


def drawGameState(board, screen):
    drawBoard(screen)
    drawPieces(board, screen)


def drawBoard(screen):
    colors = [p.Color("lightsteelblue"), p.Color("cornflowerblue")]
    for i in range(8):
        for j in range(8):
            color = colors[((i + j) % 2)]
            p.draw.rect(screen, color, p.Rect(j * square_size, i * square_size, square_size, square_size))


def drawPieces(board, screen):
    for i in range(8):
        for j in range(8):
            piece = board[i][j][:2]
            if piece != "--":
                screen.blit(images[piece], p.Rect(j * square_size, i * square_size, square_size, square_size))


if __name__ == "__main__":
    main()
