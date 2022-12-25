"""
This class is the main class responsible for running the game, setting the game to start, visualize output
and receive input from program.
"""
import pygame as p
import Move
import ChessEngine as chs
import Computation as cmp
from ChessPieces.King import King
from EndGame import EndGame

p.init()  # initialize pygame
'''
initialize board sizes and square size
'''
BOARD_HEIGHT = BOARD_WIDTH = 600
SQUARE_SIZE = 600 // 8
IMAGES = dict()
MAX_FPS = 15
setOpt = 1

Notations = []


def loadImages(images):
    """
    Loading Images
    every piece load a related image from Chess/Images/*
    """
    pieces = ["wp", "bp", "wr", "br", "wk", "bk", "wb", "bb", "wq", "bq", "wX", "bX"]  # all possible, pieces
    for i, piece in enumerate(pieces):  # for each piece load his related image
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"),
                                          (SQUARE_SIZE, SQUARE_SIZE))


def main(setOpt, engine):
    """
    def main will deal user input and update screen

    initialize 400x400 screen size and time
    """
    screen = p.display.set_mode((BOARD_HEIGHT, BOARD_WIDTH))
    time = p.time.Clock()
    screen.fill(p.Color('white'))

    """ open a new Chess engine from chessBoard && reloading pieces png"""
    loadImages(IMAGES)

    """ getting all valid moves """
    validMoves = engine.getValidMoves()
    moveMade = False

    """ creating an AI computer and an endGame checker """
    AIComputer = cmp.Computation(setOpt - 1)
    endGame = EndGame(engine)

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
                Notations.append(move.getChessNotation())
                engine.makeMove(move)  # make move
                moveMade = True
                square_selected = tuple()
                curr_move = []
            else:  # player turn
                if e.type == p.MOUSEBUTTONDOWN:  # picked a piece
                    # collect piece details
                    col, row = p.mouse.get_pos()
                    row = row // SQUARE_SIZE
                    col = col // SQUARE_SIZE
                    if square_selected == (row, col):  # clicked on the same piece twice
                        # restart player pick
                        square_selected = tuple()
                        curr_move = []
                    else:  # different pick
                        # adding pick details
                        square_selected = (row, col)
                        curr_move.append(square_selected)
                        if len(curr_move) == 1 and engine.board[row][col] is None:
                            # first pick and no piece was clicked
                            square_selected = tuple()  # restart
                            curr_move = []
                        elif len(curr_move) == 2:  # second click
                            move = Move.Move(curr_move[0], curr_move[1], engine.board)  # create move
                            for m in validMoves:
                                if move.moveID == m.moveID:
                                    print(move.getChessNotation())  # print notation
                                    Notations.append(move.getChessNotation())
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
                s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(100)
                screen.blit(s, (move.colEnd * SQUARE_SIZE, move.rowEnd * SQUARE_SIZE))
                s.fill(p.Color(255, 0, 127))
                screen.blit(s, (move.colEnd * SQUARE_SIZE, move.rowEnd * SQUARE_SIZE))


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
            p.draw.rect(screen, color, p.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # draw


def drawPieces(board, screen):
    """
    DISPLAY pieces on board
    """
    for i in range(8):
        for j in range(8):
            if board[i][j] is None:
                continue
            piece = board[i][j]  # piece pick
            screen.blit(IMAGES[piece.name[:2]], p.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def applyNotations(engine, notations):
    """
    EVAL start game positions according to given notations
    :param engine: game obj.
    :param notations: notations to modify
    """
    count = 1
    for note in notations:  # for each notation in notations
        # create and pull move according to note
        if count == 273:
            print("x")
        count += 1
        rowStart = Move.Move.rankToRow[note[1]]
        colStart = Move.Move.rankToCol[note[0]]
        rowEnd = Move.Move.rankToRow[note[3]]
        colEnd = Move.Move.rankToCol[note[2]]
        move = Move.Move((rowStart, colStart), (rowEnd, colEnd), engine.board)
        engine.makeMove(move)
        white_pos, black_pos = engine.kingPos[True], engine.kingPos[False]
        white_King = engine.board[white_pos[0]][white_pos[1]]
        black_King = engine.board[black_pos[0]][black_pos[1]]
        if not isinstance(white_King, King):
            print("x")
        if not isinstance(black_King, King):
            print("x")


def setNotations():
    """
    Insert notations to machine memo
    """
    screen = p.display.set_mode((600, 600))
    # Fill background
    background = p.Surface(screen.get_size())
    background = background.convert()
    background.fill(p.Color(255, 229, 204))

    # setting headline
    headlineFont = p.font.SysFont("Notation Adder", 60)
    headline = headlineFont.render("Notation Adder", True, p.Color("cornflowerblue"))
    headlinePos = headline.get_rect()
    headlinePos.centerx = background.get_rect().centerx

    # set sub headline
    subHeadlineFont = p.font.SysFont("Notation", 40)
    subHeadline = subHeadlineFont.render("Notation", True, p.Color("darkblue"))
    subHeadlinePos = subHeadline.get_rect()
    subHeadlinePos.x = 240
    subHeadlinePos.y = 120

    # set sub exit line
    exitLineFont = p.font.SysFont("press the exit button to go back", 30)
    exitLine = exitLineFont.render("press the exit button to go back", True, p.Color("darkblue"))
    exitLinePos = exitLine.get_rect()
    exitLinePos.x = 150
    exitLinePos.y = 400

    # set warning line
    warningFont = p.font.SysFont("WARNING", 40)
    warningLine = warningFont.render("WARNING", True, p.Color("red"))
    warningLinePos = warningLine.get_rect()
    warningLinePos.x = 240
    warningLinePos.y = 440

    # set guide line1
    guideLineFont1 = p.font.SysFont(
        "This program is not checking weather", 30)
    guideLine1 = guideLineFont1.render(
        "This program is not checking weather", True, p.Color("darkblue"))
    guideLinePos1 = guideLine1.get_rect()
    guideLinePos1.x = 120
    guideLinePos1.y = 480

    # set guide line2
    guideLineFont2 = p.font.SysFont(
        "your notations are legal or not,", 30)
    guideLine2 = guideLineFont2.render(
        "your notations are legal or not,", True, p.Color("darkblue"))
    guideLinePos2 = guideLine2.get_rect()
    guideLinePos2.x = 160
    guideLinePos2.y = 520

    # set guide line3
    guideLineFont3 = p.font.SysFont("make sure you type them correctly.", 30)
    guideLine3 = guideLineFont3.render("make sure you type them correctly.", True, p.Color("darkblue"))
    guideLinePos3 = guideLine3.get_rect()
    guideLinePos3.x = 140
    guideLinePos3.y = 560

    notationFont = p.font.Font(None, 32)
    clock = p.time.Clock()
    input_box = p.Rect(200, 160, 140, 32)
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
        screen.blit(guideLine3, guideLinePos3)
        screen.blit(warningLine, warningLinePos)
        # Blit the input_box rect.
        p.draw.rect(screen, color, input_box, 2)
        p.display.flip()
        clock.tick(30)
    return notations


def settings():
    screen = p.display.set_mode((600, 600))
    p.display.set_caption('Chess Game')

    # Fill background
    background = p.Surface(screen.get_size())
    background = background.convert()
    background.fill(p.Color(255, 229, 204))

    # Display HeadLine
    headlineFont = p.font.SysFont("Game Settings", 60)
    headline = headlineFont.render("Game Settings", True, p.Color("cornflowerblue"))
    headlinePos = headline.get_rect()
    headlinePos.centerx = background.get_rect().centerx

    subHeadlineFont = p.font.SysFont("Choose Difficulty: ", 40)
    subHeadline = subHeadlineFont.render("Choose Difficulty: ", True, p.Color("darkblue"))
    subHeadlinePos = subHeadline.get_rect()
    subHeadlinePos.x = 182
    subHeadlinePos.y = 110

    bottomHeadline = headlineFont.render("Good Luck!", True, p.Color("cornflowerblue"))
    bottomHeadlinePos = bottomHeadline.get_rect()
    bottomHeadlinePos.midbottom = background.get_rect().midbottom

    fontopt = p.font.Font(None, 35)
    opt1 = fontopt.render("Click -1- for a random component (default)", True, p.Color("darkblue"))
    opt1pos = opt1.get_rect()
    opt1pos.x = 55
    opt1pos.y = 170

    opt2 = fontopt.render("Click -2- for a level 1 component", True, p.Color("darkblue"))
    opt2pos = opt2.get_rect()
    opt2pos.x = 120
    opt2pos.y = 230

    opt3 = fontopt.render("Click -3- for a level 2 component", True, p.Color("darkblue"))
    opt3pos = opt3.get_rect()
    opt3pos.x = 120
    opt3pos.y = 290

    opt4 = fontopt.render("Click -4- for a level 3 component", True, p.Color("darkblue"))
    opt4pos = opt4.get_rect()
    opt4pos.x = 120
    opt4pos.y = 350

    editor = fontopt.render("Click -e- for a editing start positions", True, p.Color("darkblue"))
    editorPos = editor.get_rect()
    editorPos.x = 90
    editorPos.y = 410

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
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_r:
                    testNot = ['e2e3', 'd7d6', 'a2a3', 'b8a6', 'f2f3', 'a6c5', 'h2h3', 'b7b5', 'd1e2', 'a7a6', 'd2d3',
                               'g8h6', 'c1d2', 'a8a7', 'g2g4', 'c5e4', 'g4g5', 'e4c3', 'e2f2', 'e7e5', 'f2g3', 'd8d7',
                               'g3h4', 'e8e7', 'f1g2', 'e7e8', 'e3e4', 'g7g6', 'e1f2', 'd7e7', 'g2f1', 'e7e6', 'f2b6',
                               'h8g8', 'd2e3', 'e8c6', 'b1d2', 'c3e2', 'e3c5', 'f7f6', 'a1a2', 'd6c5', 'b6c6', 'e6f7',
                               'c6f6', 'f7e8', 'f6f5', 'f8g7', 'b2b4', 'c7c6', 'f5e5', 'e8d8', 'c2c3', 'e2c3', 'e5c7',
                               'd8c7', 'a3a4', 'c8e6', 'a4b5', 'c7b8', 'a2a5', 'e6h3', 'g1e2', 'c3a4', 'b5c6', 'h3d7',
                               'e2c1', 'h6f7', 'd2c4', 'g7h6', 'a5a4', 'g8h8', 'c4a3', 'd7e8', 'f3f4', 'h8f8', 'g5h6',
                               'f7h8', 'e4e5', 'a7g7', 'f1e2', 'f8f7', 'e2d1', 'g7g8', 'b4b5', 'a6a5', 'h4g5', 'e8d7',
                               'h1f1', 'f7f8', 'b5b6', 'f8f4', 'a4b4', 'd7h3', 'b6b7', 'h8f7', 'g5f4', 'g6g5', 'f4f3',
                               'g8f8', 'b4b2', 'f7h6', 'f3e3', 'h3c8', 'b2d2', 'c8g4', 'f1f2', 'f8h8', 'a3b5', 'h8f8',
                               'c1b3', 'g4e6', 'f2f7', 'f8h8', 'b3c1', 'h8f8', 'd1c2', 'c5c4', 'c1a2', 'a5a4', 'f7d7',
                               'f8f4', 'b5d6', 'e6g8', 'd2g2', 'c4d3', 'd7e7', 'f4g4', 'g2d2', 'g8b3', 'd2h2', 'a4a3',
                               'h2e2', 'g4c4', 'e3d3', 'g5g4', 'c2b1', 'c4c2', 'e7g7', 'c2c3', 'd3c3', 'h6f7', 'd6f5',
                               'b3a4', 'f5g3', 'f7h8', 'e2c2', 'h7h6', 'g7g5', 'a4c2', 'c3b4', 'c2g6', 'g3e4', 'g4g3',
                               'e4f6', 'g6c2', 'b4a5', 'c2a4', 'f6d7', 'b8c7', 'd7f6', 'a4b3', 'b1c2', 'b3d5', 'g5g3',
                               'd5c6', 'a2c3', 'a3a2', 'c2d3', 'c7b8', 'g3g4', 'a2a1', 'a5b4', 'c6d7', 'e5e6', 'a1a4',
                               'c3a4', 'd7e8', 'd3c2', 'b8b7', 'f6d7', 'b7c7', 'e6e7', 'h6h5', 'b4c5', 'e8g6', 'g4d4',
                               'g6f5', 'c5c4', 'f5c2', 'd7b8', 'c2a4', 'c4c5', 'h8g6', 'd4a4', 'g6h8', 'a4f4', 'h8f7',
                               'f4f2', 'f7h8', 'e7e8', 'h8f7', 'b8a6', 'c7b7', 'e8d7', 'b7a6', 'd7d5', 'f7d6', 'f2a2']
                    applyNotations(engine, testNot)
                    main(4, engine)
                    engine = chs.chessBoard()
                try:
                    if event.key == p.K_e:
                        notations = setNotations()
                    else:
                        if len(notations) == 0:
                            main(levelAndKey[event.key], engine)
                            engine = chs.chessBoard()
                        else:
                            applyNotations(engine, notations)
                            notations = []
                            main(levelAndKey[event.key], engine)
                            engine = chs.chessBoard()
                except Exception as e:
                    print(Notations)
                    print(e)

        screen.blit(background, (0, 0))
        p.display.flip()
    return


def simulate(engine, notations):
    """
        def main will deal user input and update screen

        initialize 400x400 screen size and time
        """
    screen = p.display.set_mode((BOARD_HEIGHT, BOARD_WIDTH))
    time = p.time.Clock()
    screen.fill(p.Color('white'))

    """ open a new Chess engine from chessBoard && reloading pieces png"""
    loadImages(IMAGES)

    """ tracking game driver """
    running = True  # boolean obj. game state end or not
    count = 0

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # if pygame is ended running turn false
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                if len(notations) == count:
                    running = False
                    break
                note = notations[count]
                count += 1
                rowStart = Move.Move.rankToRow[note[1]]
                colStart = Move.Move.rankToCol[note[0]]
                rowEnd = Move.Move.rankToRow[note[3]]
                colEnd = Move.Move.rankToCol[note[2]]
                move = Move.Move((rowStart, colStart), (rowEnd, colEnd), engine.board)
                engine.makeMove(move)
                drawBoard(screen)  # display board
                drawPieces(engine.board, screen)  # display pieces
        time.tick(MAX_FPS)
        p.display.flip()


def test(moves):
    import random
    game = chs.chessBoard()
    for i in range(1000):
        try:
            validMoves = game.getValidMoves()
            if len(validMoves) == 0:
                break
            move = random.choice(validMoves)
            moves.append(move.getChessNotation())
            game.makeMove(move)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    settings()

    # errors = []
    # for i in range(100):
    #     moves = []
    #     try:
    #         test(moves)
    #     except Exception as e:
    #         print(e)
    #         errors.append(tuple(moves))
    #
    # for error in errors:
    #     print(error)

    # testNot =
    # engine = chs.chessBoard()
    # simulate(engine=engine, notations=testNot)
    #
    # validMoves = engine.getValidMoves()
    # for move in validMoves:
    #     try:
    #         engine.makeMove(move)
    #     except Exception as e:
    #         print(e)
