"""
This class is the main class responsible for running the game, setting the game to start, visualize output
and receive input from program.
"""
import numpy as np
import pygame as p
import pygame.font

import chessEngine as chs
import Computation as cmp

p.init()  # initialize pygame
'''
initialize board sizes and square size
'''
board_height = board_width = 800
square_size = 800 // 8
images = dict()
MAX_FPS = 15
setOpt = 1


def loadImages(images):
    """
    Loading Images
    every piece load a related image from chess/Images/*
    """
    pieces = ["wp", "bp", "wr", "br", "wk", "bk", "wb", "bb", "wq", "bq", "wK", "bK"]  # all possible, pieces
    for i, piece in enumerate(pieces):  # for each piece load his related image
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"),
                                          (square_size, square_size))


def main(setOpt):
    """
    def main will deal user input and update screen

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

    """ creating an AI computer and an endGame checker """
    AIComputer = cmp.Computation(setOpt - 1)
    endGame = chs.EndGame(engine)

    """ tracking game driver """
    running = True  # boolean obj. game state end or not
    square_selected = tuple()  # will save the wanted square to be moved in each play turn
    curr_move = []  # will save the all play move, from square.... to square
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # if pygame is ended running turn false
                running = False
            if not engine.whiteTurn:
                drawGameState(engine.board, screen, (), [])
                time.tick(MAX_FPS)
                p.display.flip()
                move = AIComputer.moveCompute(engine, validMoves)
                print(move.getChessNotation())
                engine.makeMove(move)
                moveMade = True
                square_selected = tuple()
                curr_move = []
            else:
                if e.type == p.MOUSEBUTTONDOWN:
                    col, row = p.mouse.get_pos()
                    row = row // square_size
                    col = col // square_size
                    if square_selected == (row, col):
                        square_selected = tuple()
                        curr_move = []
                    else:
                        square_selected = (row, col)
                        curr_move.append(square_selected)
                        if len(curr_move) == 1 and engine.board[row][col] == "---":
                            square_selected = tuple()
                            curr_move = []
                        elif len(curr_move) == 2:
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
                square_selected = tuple()
                curr_move = []
                if len(validMoves) == 0:
                        running = False
                        print(endGame.endGame())
        drawGameState(engine.board, screen, square_selected, validMoves)
        time.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(board, screen, piece, validMoves):
    if piece != ():
        for move in validMoves:
            if move.selectedPiece == board[piece[0]][piece[1]]:
                s = p.Surface((square_size, square_size))
                s.set_alpha(100)
                screen.blit(s, (move.colEnd * square_size, move.rowEnd * square_size))
                s.fill(p.Color(255, 0, 127))
                screen.blit(s, (move.colEnd * square_size, move.rowEnd * square_size))


def drawGameState(board, screen, piece, validMoves):
    drawBoard(screen)
    highlightSquares(board, screen, piece, validMoves)
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


def settings():
    screen = p.display.set_mode((800, 800))
    p.display.set_caption('Chess Game')

    # Fill background
    background = p.Surface(screen.get_size())
    background = background.convert()
    background.fill(p.Color(255, 229, 204))

    # Display HeadLine
    headlineFont = p.font.SysFont("Game Settings", 80)
    headline = headlineFont.render("Game Settings", True, p.Color("cornflowerblue"))
    headlinePos = headline.get_rect()
    headlinePos.centerx = background.get_rect().centerx

    subHeadlineFont = p.font.SysFont("Choose Difficulty: ", 50)
    subHeadline = subHeadlineFont.render("Choose Difficulty: ", True, p.Color("darkblue"))
    subHeadlinePos = subHeadline.get_rect()
    subHeadlinePos.x = 250
    subHeadlinePos.y = 150

    bottomHeadline = headlineFont.render("Good Luck!", True, p.Color("cornflowerblue"))
    bottomHeadlinePos = bottomHeadline.get_rect()
    bottomHeadlinePos.midbottom = background.get_rect().midbottom

    fontopt = p.font.Font(None, 35)
    opt1 = fontopt.render("Click -1- for a random component (default)", True, p.Color("darkblue"))
    opt1pos = opt1.get_rect()
    opt1pos.x = 155
    opt1pos.y = 220

    opt2 = fontopt.render("Click -2- for a level 1 component", True, p.Color("darkblue"))
    opt2pos = opt2.get_rect()
    opt2pos.x = 215
    opt2pos.y = 300

    opt3 = fontopt.render("Click -3- for a level 2 component", True, p.Color("darkblue"))
    opt3pos = opt3.get_rect()
    opt3pos.x = 215
    opt3pos.y = 380

    opt4 = fontopt.render("Click -4- for a level 3 component", True, p.Color("darkblue"))
    opt4pos = opt4.get_rect()
    opt4pos.x = 215
    opt4pos.y = 460

    background.blit(bottomHeadline, bottomHeadlinePos)
    background.blit(subHeadline, subHeadlinePos)
    background.blit(headline, headlinePos)
    background.blit(opt1, opt1pos)
    background.blit(opt2, opt2pos)
    background.blit(opt3, opt3pos)
    background.blit(opt4, opt4pos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    p.display.flip()

    # Event loop
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_1:
                    main(1)
                if event.key == p.K_2:
                    main(2)
                if event.key == p.K_3:
                    main(3)
                if event.key == p.K_4:
                    main(4)

        screen.blit(background, (0, 0))
        p.display.flip()
    return


if __name__ == "__main__":
    settings()
