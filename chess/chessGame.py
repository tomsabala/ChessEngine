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
setOpt = 1

"""
Loading Images
every piece load a related image from chess/Images/*
"""


def loadImages(images):
    pieces = ["wp", "bp", "wr", "br", "wk", "bk", "wb", "bb", "wq", "bq", "wK", "bK"]  # all possible, pieces
    for i, piece in enumerate(pieces):  # for each piece load his related image
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"),
                                          (square_size, square_size))


"""
def main will deal user input and update screen
"""
def main(setOpt):
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
    square_selected = tuple()  # will save the wanted square to be moved in each play turn
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
                    if setOpt == 1:
                        move = np.random.choice(validMoves)
                        print(move.getChessNotation())
                        engine.makeMove(move)
                        moveMade = True
                        square_selected = tuple()
                        curr_move = []
                    else:
                        square_selected = (row, col)  # saving mouse click sata
                        curr_move.append(square_selected)
                        if len(curr_move) == 1 and engine.board[row][col] == "---":
                            square_selected = tuple()
                            curr_move = []
                        elif len(curr_move) == 2:  # if it's the 2-nd move
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
                    if engine.checkMate():
                        running = False
                        print("End Game")
        drawGameState(engine.board, screen, square_selected, validMoves)
        time.tick(MAX_FPS)
        p.display.flip()

def highloghtSquares(board, screen, piece, validMoves):
    if piece != ():
        for move in validMoves:
            if move.selectedPiece == board[piece[0]][piece[1]]:
                s = p.Surface((square_size, square_size))
                s.set_alpha(100)
                screen.blit(s, (move.colEnd * square_size, move.rowEnd * square_size))
                s.fill(p.Color("yellow1"))
                screen.blit(s, (move.colEnd * square_size, move.rowEnd * square_size))

def drawGameState(board, screen, piece, validMoves):
    drawBoard(screen)
    highloghtSquares(board, screen, piece, validMoves)
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
    screen = p.display.set_mode((500, 500))
    p.display.set_caption('Chess Game')

    # Fill background
    background = p.Surface(screen.get_size())
    background = background.convert()
    background.fill(p.Color("lightsteelblue"))

    # Display some text
    font = p.font.Font(None, 36)
    textHead = font.render("Game Settings:", True, p.Color("cornflowerblue"))
    textpos = textHead.get_rect()
    textpos.centerx = background.get_rect().centerx

    text002 = font.render("Choose Difficulty: ", True, p.Color("cornflowerblue"))
    text002pos = text002.get_rect()
    text002pos.x = 20
    text002pos.y = 80

    text003 = font.render("Good Luck!", True, p.Color("cornflowerblue"))
    text003pos = text003.get_rect()
    text003pos.midbottom = background.get_rect().midbottom

    fontopt = p.font.Font(None, 26)
    opt1 = fontopt.render("Click -1- for a random component (default)", True, p.Color("cornflowerblue"))
    opt1pos = opt1.get_rect()
    opt1pos.x = 50
    opt1pos.y = 130

    opt2 = fontopt.render("Click -2- for a level 1 component", True, p.Color("cornflowerblue"))
    opt2pos = opt2.get_rect()
    opt2pos.x = 50
    opt2pos.y = 160

    opt3 = fontopt.render("Click -3- for a level 2 component", True, p.Color("cornflowerblue"))
    opt3pos = opt3.get_rect()
    opt3pos.x = 50
    opt3pos.y = 190

    opt4 = fontopt.render("Click -4- for a level 3 component", True, p.Color("cornflowerblue"))
    opt4pos = opt4.get_rect()
    opt4pos.x = 50
    opt4pos.y = 220

    background.blit(text003, text003pos)
    background.blit(text002, text002pos)
    background.blit(textHead, textpos)
    background.blit(opt1, opt1pos)
    background.blit(opt2, opt2pos)
    background.blit(opt3, opt3pos)
    background.blit(opt4, opt4pos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    p.display.flip()

    # Event loop
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                return
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
