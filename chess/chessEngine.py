"""
this class responsible for
generate moves
board evaluation
minimax
and alpha beta pruning
"""
import numpy as np


class chessBoard:
    def __init__(self):
        """
        presenting board as 8X8 np array,
        blank spot - "--",
        white piece - "w_", black piece - "b_",
        Rook, Knight, Bishop etc. - "_r", "_k", "_b" and so on.
        """
        self.board = np.array([["br1", "bk1", "bb1", "bK", "bq", "bb2", "bk2", "br2"],
                               ["bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"],
                               ["---", "---", "---", "---", "---", "---", "---", "---"],
                               ["---", "---", "---", "---", "---", "---", "---", "---"],
                               ["---", "---", "---", "---", "---", "---", "---", "---"],
                               ["---", "---", "---", "---", "---", "---", "---", "---"],
                               ["wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"],
                               ["wr1", "wk1", "wb1", "wK", "wq", "wb2", "wk2", "wr2"]])
        self.blackPieces = {"br1": (0, 0), "bk1": (0, 1), "bb1": (0, 2), "bK": (0, 3), "bq": (0, 4)
            , "bb2": (0, 5), "bk2": (0, 6), "br2": (0, 7)
            , "bp1": (1, 0), "bp2": (1, 1), "bp3": (1, 2), "bp4": (1, 3), "bp5": (1, 4)
            , "bp6": (1, 5), "bp7": (1, 6), "bp8": (1, 7)}
        self.whitePieces = {"wr1": (7, 0), "wk1": (7, 1), "wb1": (7, 2), "wK": (7, 3), "wq": (7, 4)
            , "wb2": (7, 5), "wk2": (7, 6), "wr2": (7, 7)
            , "wp1": (6, 0), "wp2": (6, 1), "wp3": (6, 2), "wp4": (6, 3), "wp5": (6, 4)
            , "wp6": (6, 5), "wp7": (6, 6), "wp8": (6, 7)}
        self.whiteTurn = True  # a boolean obj. for whose turn is it
        self.moveLog = np.array([])  # an array of all moves

    def makeMove(self, move):
        """
        initial move as a play on the board
        """
        if move.castling:
            pass
        elif move.enPassant:
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece
            self.board[move.rowStart][move.colStart] = "---"
            self.board[move.rowStart][move.colEnd] = "---"
            if self.whiteTurn:
                self.whitePieces[move.selectedPiece] = move.rowEnd, move.colEnd
                del self.blackPieces[move.capturedPiece]
            else:
                self.blackPieces[move.selectedPiece] = move.rowEnd, move.colEnd
                del self.whitePieces[move.capturedPiece]
        else:
            self.board[move.rowStart][move.colStart] = "---"  # last position becomes empty
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece  # selected piece moving to the next position
            if self.whiteTurn:
                self.whitePieces[move.selectedPiece] = move.rowEnd, move.colEnd
                if move.capturedPiece in self.blackPieces.keys():
                    del self.blackPieces[move.capturedPiece]
            else:
                self.blackPieces[move.selectedPiece] = move.rowEnd, move.colEnd
                if move.capturedPiece in self. whitePieces.keys():
                    del self.whitePieces[move.capturedPiece]
        self.moveLog = np.append(self.moveLog, move)  # appending the move to memory
        self.whiteTurn = not self.whiteTurn  # switching turns


    def undoMove(self):
        """
        resetting board to last move
        """
        if len(self.moveLog) > 0:  # there is a move to undo
            move = self.moveLog[-1]  # last move in the array
            if move.castling:
                pass
            elif move.enPassant:
                self.board[move.rowEnd][move.colEnd] = "---"
                self.board[move.rowStart][move.colStart] = move.selectedPiece
                self.board[move.rowStart][move.colEnd] = move.capturedPiece
                if not self.whiteTurn:
                    self.blackPieces[move.capturedPiece] = move.rowEnd, move.colStart
                    self.whitePieces[move.selectedPiece] = move.rowStart, move.colStart
                else:
                    self.whitePieces[move.capturedPiece] = move.rowEnd, move.colStart
                    self.blackPieces[move.selectedPiece] = move.rowStart, move.colStart
            # resetting the board
            else:
                self.board[move.rowEnd][move.colEnd] = move.capturedPiece
                self.board[move.rowStart][move.colStart] = move.selectedPiece
                if move.capturedPiece != "---":
                    if not self.whiteTurn:
                        self.blackPieces[move.capturedPiece] = move.rowEnd, move.colEnd
                        self.whitePieces[move.selectedPiece] = move.rowStart, move.colStart
                    else:
                        self.blackPieces[move.selectedPiece] = move.rowStart, move.colStart
                        self.whitePieces[move.capturedPiece] = move.rowEnd, move.colEnd
                else:
                    if not self.whiteTurn:
                        self.whitePieces[move.selectedPiece] = move.rowStart, move.colStart
                    else:
                        self.blackPieces[move.selectedPiece] = move.rowStart, move.colStart
            self.whiteTurn = not self.whiteTurn
            self.moveLog = np.delete(self.moveLog, len(self.moveLog) - 1)

    def getValidMoves(self):
        validPawnMove = np.array([])
        if self.whiteTurn:
            tmpDict = dict.copy(self.whitePieces)
            for piece in tmpDict.items():
                if piece[0][:2] == "wp":
                    validPawnMove = np.append(validPawnMove, self.legalMovePawn(self.board, piece[1]))
        else:
            tmpDict = dict.copy(self.blackPieces)
            for piece in tmpDict.items():
                if piece[0][:2] == "bp":
                    validPawnMove = np.append(validPawnMove, self.legalMovePawn(self.board, piece[1], False))
        return validPawnMove

    """
    return a list of all valid move for a certain pawn on board
    """

    def legalMovePawn(self, board, piece, white=True):
        row, col = piece[0], piece[1]
        validMoves = np.array([])
        rul = Rules(board)
        if white:
            if row == 6:
                if board[row - 1][col] == "---":
                    tmpMove = Move((row, col), (row - 1, col), board)
                    self.makeMove(tmpMove)
                    if not rul.isCheck(board, self.whitePieces["wK"], white):
                        validMoves = np.append(validMoves, tmpMove)
                    self.undoMove()
                    if board[row - 2][col] == "---":
                        tmpMove = Move((row, col), (row - 2, col), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.whitePieces["wK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                if col - 1 >= 0:
                    if board[row - 1][col - 1][0] == "b":
                        tmpMove = Move((row, col), (row - 1, col - 1), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.whitePieces["wK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                if col + 1 <= 7:
                    if board[row - 1][col + 1][0] == "b":
                        tmpMove = Move((row, col), (row - 1, col + 1), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.whitePieces["wK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
            elif row - 1 >= 0:
                if board[row - 1][col] == "---":
                    tmpMove = Move((row, col), (row - 1, col), board)
                    self.makeMove(tmpMove)
                    if not rul.isCheck(board, self.whitePieces["wK"], white):
                        validMoves = np.append(validMoves, tmpMove)
                    self.undoMove()
                if col - 1 >= 0:
                    if board[row - 1][col - 1][0] == "b":
                        tmpMove = Move((row, col), (row - 1, col - 1), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.whitePieces["wK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                    if (row == 3) and board[row][col - 1][:2] == "bp":
                        tmpMove = Move((row, col), (row - 1, col - 1), board, True)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.whitePieces["wK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                if col + 1 <= 7:
                    if board[row - 1][col + 1][0] == "b":
                        tmpMove = Move((row, col), (row - 1, col + 1), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.whitePieces["wK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                    if (row == 3) and board[row][col + 1][:2] == "bp":
                        tmpMove = Move((row, col), (row - 1, col + 1), board, True)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.whitePieces["wK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
        else:
            if row == 1:
                if board[row + 1][col] == "---":
                    tmpMove = Move((row, col), (row + 1, col), board)
                    self.makeMove(tmpMove)
                    if not rul.isCheck(board, self.blackPieces["bK"], white):
                        validMoves = np.append(validMoves, tmpMove)
                    self.undoMove()
                    if board[row + 2][col] == "---":
                        tmpMove = Move((row, col), (row + 2, col), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.blackPieces["bK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                if col - 1 >= 0:
                    if board[row + 1][col - 1][0] == "w":
                        tmpMove = Move((row, col), (row + 1, col - 1), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.blackPieces["bK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                if col + 1 <= 7:
                    if board[row + 1][col + 1][0] == "w":
                        tmpMove = Move((row, col), (row + 1, col + 1), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.blackPieces["bK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
            elif row + 1 <= 7:
                if board[row + 1][col] == "---":
                    tmpMove = Move((row, col), (row + 1, col), board)
                    self.makeMove(tmpMove)
                    if not rul.isCheck(board, self.blackPieces["bK"], white):
                        validMoves = np.append(validMoves, tmpMove)
                    self.undoMove()
                if col - 1 >= 0:
                    if board[row + 1][col - 1][0] == "w":
                        tmpMove = Move((row, col), (row + 1, col - 1), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.blackPieces["bK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                    if row == 4 and board[row][col - 1][:2] == "wp":
                        tmpMove = Move((row, col), (row + 1, col - 1), board, True)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.blackPieces["bK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                if col + 1 <= 7:
                    if board[row + 1][col + 1][0] == "w":
                        tmpMove = Move((row, col), (row + 1, col + 1), board)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.blackPieces["bK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
                    if row == 4 and board[row][col + 1][:2] == "wp":
                        tmpMove = Move((row, col), (row + 1, col + 1), board, True)
                        self.makeMove(tmpMove)
                        if not rul.isCheck(board, self.blackPieces["bK"], white):
                            validMoves = np.append(validMoves, tmpMove)
                        self.undoMove()
        return validMoves


class Move:
    """
    this class responsible for evaluating move and generating move annotations and valid moves
    """
    # form dictionaries: from annotations to position and the opposite way
    rankToRow = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowToRank = {v: k for k, v in rankToRow.items()}
    rankToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colToRank = {v: k for k, v in rankToCol.items()}

    def __int__(self):
        self.rowStart = None
        self.colStart = None
        self.rowEnd = None
        self.colEnd = None
        self.selectedPiece = None
        self.capturedPiece = None
        self.moveID = None

    # initial a new move
    def __init__(self, startLoc, endLoc, board, enPassant=False, castling=False):
        # where from
        self.rowStart = startLoc[0]
        self.colStart = startLoc[1]
        # where to
        self.rowEnd = endLoc[0]
        self.colEnd = endLoc[1]
        if self.isEnPassant(board, startLoc, endLoc) or enPassant:
            self.enPassant = True
        else:
            self.enPassant = False
        # pieces involved
        self.selectedPiece = board[self.rowStart][self.colStart]
        if self.enPassant:
            self.capturedPiece = board[self.rowStart][self.colEnd]
        else:
            self.capturedPiece = board[self.rowEnd][self.colEnd]
        self.castling = castling
        self.moveID = 100000 * self.castling + 10000 * self.enPassant + 1000 * self.rowStart + 100 * self.colStart + 10 * self.rowEnd + 1 * self.colEnd

    def isEnPassant(self, board, startLoc, endLoc):
        if startLoc[0] == 3:
            if board[startLoc[0]][startLoc[1]][:2] == "wp":
                if board[endLoc[0]][endLoc[1]] == "---":
                    if board[startLoc[0]][endLoc[1]][:2] == "bp":
                        return True
        elif startLoc[0] == 4:
            if board[startLoc[0]][startLoc[1]][:2] == "bp":
                if board[endLoc[0]][endLoc[1]] == "---":
                    if board[startLoc[0]][endLoc[1]][:2] == "wp":
                        return True
        return False
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    def getChessNotation(self):  # saving the move notation
        return self.getRankStr(self.rowStart, self.colStart) + self.getRankStr(self.rowEnd, self.colEnd)

    def getRankStr(self, row, col):
        return self.colToRank[col] + self.rowToRank[row]


class Rules:
    def __init__(self, board):
        self.board = board

    """
        checking whether the king is threaten
    """

    def isCheck(self, board, kingPos, white=True):
        return self.isInThreat(board, kingPos, white)

    def isInThreat(self, board, piece, white=True):
        """
        :param board: current board status
        :param piece: piece to be check, a tuple of 2 integers represents the place on the board
        :param white: a boolean to check whether black is threaten by or white is
        :return: boolean obj. True iff is threaten
        """
        # checking if there is a threat on the diagnols
        posDiagnol = self.downRightDiagnol(board, piece, white) or self.downLeftDiagnol(board, piece, white) or \
                     self.upLeftDiagnol(board, piece, white) or self.upRightDiagnol(board, piece, white)
        # checking if there is a threat on the vertical
        posVertical = self.verticalUp(board, piece, white) or self.verticalDown(board, piece, white)
        # checking if there is a threat on the horizon
        posHorizon = self.horizonLeft(board, piece, white) or self.horizonRight(board, piece, white)
        # checking if there is a threat from a knight
        posKnightMoves = self.KnightMoves(board, piece, white)
        return posHorizon or posVertical or posDiagnol or posKnightMoves

    """
    all 9 next functions are checking if when given a certain piece and color, 
    that piece is threaten by the opposite player pieces from diagnol, vertical, horizon or a knight
    """

    def KnightMoves(self, board, piece, white):
        """
        """
        row, col = piece[0], piece[1]
        whiteKnights = {"wk1", "wk2"}
        blackKnights = {"bk1", "bk2"}
        knightAhead = []
        knightTuppleInd = {(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)}
        for tup in knightTuppleInd:
            if (0 <= row + tup[0] <= 7) and (0 <= col + tup[1] <= 7):
                currPos = board[row + tup[0]][col + tup[1]]
                knightAhead.append(currPos)
        # seeing if there is a match between black knight and white king or opposite
        if white and len(set(knightAhead).intersection(blackKnights)) > 0:
            return True
        elif not white and len(set(knightAhead).intersection(whiteKnights)) > 0:
            return True
        return False

    def downRightDiagnol(self, board, position, white=True):
        row, col = position[0], position[1]
        i = 1
        while 0 <= row + i <= 7 and 0 <= col + i <= 7:
            currPos = board[row + i][col + i]
            if white:
                if currPos in {"bq", "bb1", "bb2"} or (i == 1 and currPos[:2] == "bK"):
                    return True
                elif currPos != "--":
                    break
            else:
                if currPos in {"wq", "wb1", "wb2"} or (i == 1 and currPos[:2] in {"wp", "wK"}):
                    return True
                elif currPos != "--":
                    break
            i += 1
        return False

    def downLeftDiagnol(self, board, position, white=True):
        row, col = position[0], position[1]
        i = 1
        j = -1
        while 0 <= row + i <= 7 and 0 <= col + j <= 7:
            currPos = board[row + i][col + j]
            if white:
                if currPos in {"bq", "bb1", "bb2"} or (i == 1 and j == -1 and currPos[:2] == "bK"):
                    return True
                elif currPos != "--":
                    break
            else:
                if currPos in {"wq", "wb1", "wb2"} or (i == 1 and j == -1 and currPos[:2] in {"wp", "wK"}):
                    return True
                elif currPos != "--":
                    break
            j -= 1
            i += 1
        return False

    def upLeftDiagnol(self, board, position, white=True):
        row, col = position[0], position[1]
        i = -1
        while 0 <= row + i <= 7 and 0 <= col + i <= 7:
            currPos = board[row + i][col + i]
            if white:
                if currPos in {"bq", "bb1", "bb2"} or (i == -1 and currPos[:2] in {"bp", "bK"}):
                    return True
                elif currPos != "--":
                    break
            else:
                if currPos in {"wq", "wb1", "wb2"} or (i == -1 and currPos[:2] == "wK"):
                    return True
                elif currPos != "--":
                    break
            i -= 1
        return False

    def upRightDiagnol(self, board, position, white=True):
        row, col = position[0], position[1]
        i = -1
        j = 1
        while 0 <= row + i <= 7 and 0 <= col + j <= 7:
            currPos = board[row + i][col + j]
            if white:
                if currPos in {"bq", "bb1", "bb2"} or (i == -1 and j == 1 and currPos[:2] in {"bp", "bK"}):
                    return True
                elif currPos != "---":
                    break
            else:
                if currPos in {"wq", "wb1", "wb2"} or (i == -1 and j == 1 and currPos[:2] == "wK"):
                    return True
                elif currPos != "---":
                    break
            j += 1
            i -= 1
        return False

    def horizonRight(self, board, position, white=True):
        row, col = position[0], position[1]
        i = 1
        while 0 <= col + i <= 7:
            currPos = board[row][col + i]
            if white:
                if currPos in {"bq", "br1", "br2"} or (i == 1 and currPos[:2] == "bK"):
                    return True
                elif currPos != "---":
                    break
            else:
                if currPos in {"wq", "wr1", "wr2"} or (i == 1 and currPos[:2] == "wK"):
                    return True
                elif currPos != "---":
                    break
            i += 1
        return False

    def horizonLeft(self, board, position, white=True):
        row, col = position[0], position[1]
        j = -1
        while 0 <= col + j <= 7:
            currPos = board[row][col + j]
            if white:
                if currPos in {"bq", "br1", "br2"} or (j == -1 and currPos[:2] == "bK"):
                    return True
                elif currPos != "---":
                    break
            else:
                if currPos in {"wq", "wr1", "wr2"} or (j == -1 and currPos[:2] == "wK"):
                    return True
                elif currPos != "---":
                    break
            j -= 1
        return False

    def verticalDown(self, board, position, white=True):
        row, col = position[0], position[1]
        i = 1
        while 0 <= row + i <= 7:
            currPos = board[row + i][col]
            if white:
                if currPos in {"bq", "br1", "br2"} or (i == 1 and currPos[:2] == "bK"):
                    return True
                elif currPos != "---":
                    break
            else:
                if currPos in {"wq", "wr1", "wr2"} or (i == 1 and currPos[:2] == "wK"):
                    return True
                elif currPos != "---":
                    break
            i += 1
        return False

    def verticalUp(self, board, position, white=True):
        row, col = position[0], position[1]
        j = -1
        while 0 <= row + j <= 7:
            currPos = board[row + j][col]
            if white:
                if currPos in {"bq", "br1", "br2"} or (j == -1 and currPos[:2] == "bK"):
                    return True
                elif currPos != "---":
                    break
            else:
                if currPos in {"wq", "wr1", "wr2"} or (j == -1 and currPos[:2] == "wK"):
                    return True
                elif currPos != "---":
                    break
            j -= 1
        return False

