"""
This class is the main class responsible for running the game, setting the game to start, visualize output
and receive input from program.
"""
import pygame as p
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


def main(setOpt, engine):
    """
    def main will deal user input and update screen

    initialize 400x400 screen size and time
    """
    screen = p.display.set_mode((board_height, board_width))
    time = p.time.Clock()
    screen.fill(p.Color('white'))

    """ open a new chess engine from chessBoard && reloading pieces png"""
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
            if not engine.whiteTurn and setOpt != 0:  # opponents turn
                drawGameState(engine.board, screen, (), [])  # draw game state
                time.tick(MAX_FPS)
                p.display.flip()
                move = AIComputer.moveCompute(engine, validMoves)  # generate move
                print(move.getChessNotation())  # display move annotation
                engine.makeMove(move)  # make move
                moveMade = True
                square_selected = tuple()
                curr_move = []
            else:  # player turn
                if e.type == p.MOUSEBUTTONDOWN:  # picked a piece
                    # collect piece details
                    col, row = p.mouse.get_pos()
                    row = row // square_size
                    col = col // square_size
                    if square_selected == (row, col):  # clicked on the same piece twice
                        # restart player pick
                        square_selected = tuple()
                        curr_move = []
                    else:  # different pick
                        # adding pick details
                        square_selected = (row, col)
                        curr_move.append(square_selected)
                        if len(curr_move) == 1 and engine.board[row][col] == "---":
                            # first pick and no piece was clicked
                            square_selected = tuple()  # restart
                            curr_move = []
                        elif len(curr_move) == 2:  # second click
                            move = chs.Move(curr_move[0], curr_move[1], engine.board)  # create move
                            if move in validMoves:  # if move is legal
                                print(move.getChessNotation())  # print notation
                                engine.makeMove(move)  # make move
                                moveMade = True
                            square_selected = tuple()
                            curr_move = []
                elif e.type == p.KEYDOWN:  # keyboard click
                    if e.key == p.K_z:  # reverse click, undo
                        try:
                            engine.undoMove(engine.moveLog[-1])
                            moveMade = True
                            square_selected = tuple()
                            curr_move = []
                        except IndexError:
                            pass
            if moveMade:  # if move was made
                moveMade = False
                validMoves = engine.getValidMoves()  # generate valid moves
                square_selected = tuple()
                curr_move = []
                if len(validMoves) == 0:  # no legal moves available
                    # end game
                    running = False
                    print(endGame.endGame(engine.kingPos[engine.whiteTurn]).value)
        drawGameState(engine.board, screen, square_selected, validMoves)  # draw game state
        time.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(board, screen, piece, validMoves):
    """
    DISPLAY highlighted squares
    """
    if piece != ():
        for move in validMoves:
            if move.selectedPiece == board[piece[0]][piece[1]]:
                s = p.Surface((square_size, square_size))
                s.set_alpha(100)
                screen.blit(s, (move.colEnd * square_size, move.rowEnd * square_size))
                s.fill(p.Color(255, 0, 127))
                screen.blit(s, (move.colEnd * square_size, move.rowEnd * square_size))


def drawGameState(board, screen, piece, validMoves):
    """
    DISPLAY draw game board, pieces, and annotations
    :param board: current board status
    :param screen: screen board
    :param piece: active piece
    :param validMoves: piece valid moves
    """
    drawBoard(screen)  # display board
    highlightSquares(board, screen, piece, validMoves)  # highlight piece moves
    drawPieces(board, screen)  # display pieces


def drawBoard(screen):
    """
    DISPLAY draw board table
    """
    colors = [p.Color("lightsteelblue"), p.Color("cornflowerblue")]  # colors
    for i in range(8):
        for j in range(8):
            color = colors[((i + j) % 2)]  # color pick
            p.draw.rect(screen, color, p.Rect(j * square_size, i * square_size, square_size, square_size))  # draw


def drawPieces(board, screen):
    """
    DISPLAY pieces on board
    """
    for i in range(8):
        for j in range(8):
            piece = board[i][j][:2]  # piece pick
            if piece != "--":
                screen.blit(images[piece], p.Rect(j * square_size, i * square_size, square_size, square_size))  # draw


def applyNotations(engine, notations):
    """
    EVAL start game positions according to given notations
    :param engine: game obj.
    :param notations: notations to modify
    """
    for note in notations:  # for each notation in notations
        # create and pull move according to note
        rowStart = chs.Move.rankToRow[note[1]]
        colStart = chs.Move.rankToCol[note[0]]
        rowEnd = chs.Move.rankToRow[note[3]]
        colEnd = chs.Move.rankToCol[note[2]]
        move = chs.Move((rowStart, colStart), (rowEnd, colEnd), engine.board)
        engine.makeMove(move)


def setNotations():
    """
    Insert notations to machine memo
    """
    screen = p.display.set_mode((800, 800))
    # Fill background
    background = p.Surface(screen.get_size())
    background = background.convert()
    background.fill(p.Color(255, 229, 204))

    # setting headline
    headlineFont = p.font.SysFont("Notation Adder", 80)
    headline = headlineFont.render("Notation Adder", True, p.Color("cornflowerblue"))
    headlinePos = headline.get_rect()
    headlinePos.centerx = background.get_rect().centerx

    # set sub headline
    subHeadlineFont = p.font.SysFont("Notation", 50)
    subHeadline = subHeadlineFont.render("Notation", True, p.Color("darkblue"))
    subHeadlinePos = subHeadline.get_rect()
    subHeadlinePos.x = 327
    subHeadlinePos.y = 250

    # set sub exit line
    exitLineFont = p.font.SysFont("press the exit button to go back", 30)
    exitLine = exitLineFont.render("press the exit button to go back", True, p.Color("darkblue"))
    exitLinePos = exitLine.get_rect()
    exitLinePos.x = 250
    exitLinePos.y = 760

    # set warning line
    warningFont = p.font.SysFont("WARNING", 40)
    warningLine = warningFont.render("WARNING", True, p.Color("red"))
    warningLinePos = warningLine.get_rect()
    warningLinePos.x = 335
    warningLinePos.y = 600

    # set guide line1
    guideLineFont1 = p.font.SysFont(
        "This program is not checking weather your notations are legal or not,", 30)
    guideLine1 = guideLineFont1.render(
        "This program is not checking weather your notations are legal or not,", True, p.Color("darkblue"))
    guideLinePos1 = guideLine1.get_rect()
    guideLinePos1.x = 60
    guideLinePos1.y = 640

    # set guide line2
    guideLineFont2 = p.font.SysFont("make sure you type them right", 30)
    guideLine2 = guideLineFont2.render("make sure you type them right", True, p.Color("darkblue"))
    guideLinePos2 = guideLine2.get_rect()
    guideLinePos2.x = 250
    guideLinePos2.y = 680

    notationFont = p.font.Font(None, 32)
    clock = p.time.Clock()
    input_box = p.Rect(300, 300, 140, 32)
    color_inactive = p.Color('darkblue')
    color_active = p.Color('cornflowerblue')
    color = color_inactive
    active = False
    done = False

    notations = []
    currNot = ""
    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
            if event.type == p.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == p.KEYDOWN:
                if active:
                    if event.key == p.K_RETURN:
                        notations.append(currNot)
                        currNot = ""
                    elif event.key == p.K_BACKSPACE:
                        currNot = currNot[:-1]
                    else:
                        currNot += event.unicode

        screen.fill((255, 229, 204))
        # Render the current text.
        txt_surface = notationFont.render(currNot, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        screen.blit(headline, headlinePos)
        screen.blit(subHeadline, subHeadlinePos)
        screen.blit(exitLine, exitLinePos)
        screen.blit(guideLine1, guideLinePos1)
        screen.blit(guideLine2, guideLinePos2)
        screen.blit(warningLine, warningLinePos)
        # Blit the input_box rect.
        p.draw.rect(screen, color, input_box, 2)
        p.display.flip()
        clock.tick(30)
    return notations


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

    editor = fontopt.render("Click -e- for a editing start positions", True, p.Color("darkblue"))
    editorPos = editor.get_rect()
    editorPos.x = 195
    editorPos.y = 540

    background.blit(bottomHeadline, bottomHeadlinePos)
    background.blit(subHeadline, subHeadlinePos)
    background.blit(headline, headlinePos)
    background.blit(opt1, opt1pos)
    background.blit(opt2, opt2pos)
    background.blit(opt3, opt3pos)
    background.blit(opt4, opt4pos)
    background.blit(editor, editorPos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    p.display.flip()

    # creating engine
    engine = chs.chessBoard()
    # Event loop
    running = True
    # crating level dictionary
    levelAndKey = {p.K_0: 0, p.K_1: 1, p.K_2: 2, p.K_3: 3, p.K_4: 4, p.K_e: setNotations}
    notations = []
    while running:
        engine = chs.chessBoard()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_r:
                    testNot = ["g1f3", "b8c6", "e2e3", "g8f6", "f3d4", "d7d5", "f2f3", "e7e5", "e1h4", "e5d4", "e3d4", "c6d4", "d2d3", "e8a4", "c1g5", "a4c2", "d1e1", "f8b4"]
                    applyNotations(engine, testNot)
                    main(4, engine)
                try:
                    if event.key == p.K_e:
                        notations = setNotations()
                    else:
                        if len(notations) == 0:
                            main(levelAndKey[event.key], engine)
                        else:
                            applyNotations(engine, notations)
                            notations = []
                            main(levelAndKey[event.key], engine)
                except KeyError:
                    pass

        screen.blit(background, (0, 0))
        p.display.flip()
    return


if __name__ == "__main__":
    settings()
