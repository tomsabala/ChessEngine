import math
import random

from chess import *
import numpy as np


class Computation:
    piecesScore = {"K": 100, "q": 10, "r": 5,
                   "b": 3, "k": 3, "p": 1}
    whiteKingControl = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                        [-2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]
    whiteQueenControl = [[-2.0, -2.0, -1.0, -0.5, -0.5, -1.0, -2.0, -2.0],
                         [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                         [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                         [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                         [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0],
                         [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -1.0],
                         [-1.0, 0.0, 0.5, 0.0, 0.0, 0.5, 0.0, -1.0],
                         [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]
    whiteRookControl = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]
    whiteBishopControl = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                          [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                          [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                          [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                          [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                          [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                          [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                          [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]
    whiteKnightControl = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                          [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                          [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                          [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                          [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                          [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                          [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                          [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]
    whitePawnControl = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    blackKingControl = whiteKingControl[::-1]
    blackQueenControl = whiteQueenControl[::-1]
    blackRookControl = whiteRookControl[::-1]
    blackBishopControl = whiteBishopControl[::-1]
    blackKnightControl = whiteKnightControl[::-1]
    blackPawnControl = whitePawnControl[::-1]
    piecesControl = {"wp": whitePawnControl, "wr": whiteRookControl, "wb": whiteBishopControl,
                         "wk": whiteKnightControl, "wq": whiteQueenControl, "wK": whiteKingControl,
                         "bp": blackPawnControl, "br": blackRookControl, "bb": blackBishopControl,
                         "bk": blackKnightControl, "bq": blackQueenControl, "bK": blackKingControl}

    def __init__(self, level):
        self.lvl = level

    def moveCompute(self, engine, validMoves):
        if self.lvl == 0:
            move = np.random.choice(validMoves)
            return move
        elif self.lvl == 1:
            return self.depth1(engine, validMoves)
        elif self.lvl == 2:
            return self.depth2(engine, validMoves)
        else:
            return self.depth3(engine, validMoves)

    def depth1(self, engine, validMoves):
        minScore = math.inf
        moveBank = []
        for move in validMoves:
            engine.makeMove(move, True)
            whiteScore = self.materialPieces(engine, True)
            engine.undoMove(True)
            if whiteScore < minScore:
                moveBank = [move]
                minScore = whiteScore
            elif whiteScore == minScore:
                moveBank.append(move)
        return moveBank[random.randint(0, len(moveBank)-1)]

    def depth2(self, engine, validMoves):
        pass

    def depth3(self, engine, validMoves):
        pass

    def materialPieces(self, engine, white):
        whiteScore = 0
        blackScore = 0
        for piece in engine.whitePieces:
            whiteScore += self.piecesScore[piece[1]]
        for piece in engine.blackPieces:
            blackScore += self.piecesScore[piece[1]]
        if white:
            return whiteScore
        else:
            return blackScore

    def boardControl(self, engine, white):
        whiteScore = 0
        blackScore = 0
        for piece, pos in engine.whitePieces.items():
            if piece[0] == "w":
                whiteScore += self.piecesControl[piece[:2]][pos[0]][pos[1]]
            else:
                blackScore += self.piecesControl[piece[:2]][pos[0]][pos[1]]
        if white:
            return whiteScore
        else:
            return blackScore
