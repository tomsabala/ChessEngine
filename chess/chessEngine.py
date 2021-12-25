"""
this class responsible for
generate moves
board evaluation
minimax
and alpha beta pruning
"""
import numpy as np
from enum import Enum


class EndGame:
    """
    class responsible for determining the end game result
    it is nly been used if a certain player has no further moves.
    and return's Enum values only.
    """
    def __init__(self, engine):
        self.engine = engine

    class end(Enum):
        WHITE = "End game, White loose"
        BLACK = "End game, Black loose"
        DRAW = "End game, It's a draw"

    def endGame(self):
        """
        functions will be called only when player has no moves available
        and will check if king is on threat
        :return: boolean value true iff check-mate
        """
        rul = Rules()
        if self.engine.whiteTurn and rul.isCheck(self.engine.board, self.engine.whitePieces["wK"], self.engine.whiteTurn):
            return self.end.WHITE
        elif not self.engine.whiteTurn and rul.isCheck(self.engine.board, self.engine.blackPieces["bK"], False):
            return self.end.BLACK
        return self.end.DRAW


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
        # black and white pieces' dictionary for positions etc. uses to eval game state
        self.blackPieces = {"br1": (0, 0), "bk1": (0, 1), "bb1": (0, 2), "bK": (0, 3), "bq": (0, 4), "bb2": (0, 5),
                            "bk2": (0, 6), "br2": (0, 7), "bp1": (1, 0), "bp2": (1, 1), "bp3": (1, 2), "bp4": (1, 3),
                            "bp5": (1, 4), "bp6": (1, 5), "bp7": (1, 6), "bp8": (1, 7)}
        self.whitePieces = {"wr1": (7, 0), "wk1": (7, 1), "wb1": (7, 2), "wK": (7, 3), "wq": (7, 4), "wb2": (7, 5),
                            "wk2": (7, 6), "wr2": (7, 7), "wp1": (6, 0), "wp2": (6, 1), "wp3": (6, 2), "wp4": (6, 3),
                            "wp5": (6, 4), "wp6": (6, 5), "wp7": (6, 6), "wp8": (6, 7)}
        # castle status dictionary-log
        self.Castle = {"bK": True, "br1": True, "br2": True, "wK": True, "wr1": True, "wr2": True}
        self.dictCastleLog = {}
        # game turn-log
        self.whiteTurn = True  # a boolean obj. for whose turn is it
        self.moveLog = np.array([])  # an array of all moves

    def makeMove(self, move, check=False):
        """
        initial move as a play on the board
        """
        # updating board
        self.updateBoard(move)
        # updating piece and castle dictionary
        if not check:
            self.updatePieces(move, self.whiteTurn)
        self.moveLog = np.append(self.moveLog, move)  # appending the move to memory
        self.whiteTurn = not self.whiteTurn  # switching turns

    def updateBoard(self, move):
        """
        updating board according to move annotation, after a move is done
        :param move: Move type object
        :return: None
        """
        if move.castling:  # for a castling move
            # updating king position on board
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece
            self.board[move.rowStart][move.colStart] = "---"
            # updating rook position on board
            if move.colEnd < move.colStart:  # for a left side castling
                self.board[move.rowEnd][move.colEnd + 1] = move.capturedPiece
                self.board[move.rowStart][0] = "---"
            else:  # for a right side castling
                self.board[move.rowEnd][move.colEnd - 1] = move.capturedPiece
                self.board[move.rowStart][7] = "---"

        elif move.enPassant:  # for an en-passant move
            # updating selected and captured positions on board
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece
            self.board[move.rowStart][move.colStart] = "---"
            self.board[move.rowStart][move.colEnd] = "---"
        elif move.promotion:  # for a promotion move
            # updating piece presenting + updating board position
            move.selectedPiece = move.selectedPiece[0] + "qp" + move.selectedPiece[-1]
            self.board[move.rowStart][move.colStart] = "---"
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece
        else:  # for a regular move
            # updating selected piece position
            self.board[move.rowStart][move.colStart] = "---"
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece

    def updatePieces(self, move, white):
        """
        updating pieces dictionaries according to move annotation, after a move is made
        :param move: Move type object
        :param white: boolean type, True iff move is a white piece move
        :return: None
        """
        # boolean to piece color dictionary
        dictTurnUpdates = {True: self.whitePieces, False: self.blackPieces}
        if move.castling:  # for a castling move
            # updating king piece
            dictTurnUpdates[white][move.selectedPiece] = move.rowEnd, move.colEnd
            # updating rook piece
            if move.colEnd < move.colStart:  # left side castling
                dictTurnUpdates[white][move.capturedPiece] = move.rowEnd, move.colEnd + 1
            else:  # right side castling
                dictTurnUpdates[white][move.capturedPiece] = move.rowEnd, move.colEnd - 1
            # updating castling state dictionary
            self.dictCastleLog[move.moveID] = self.Castle.copy()
            self.Castle[move.capturedPiece] = False
            self.Castle[move.selectedPiece] = False
        elif move.enPassant:  # for an an-passant move
            # updating selected piece
            dictTurnUpdates[white][move.selectedPiece] = move.rowEnd, move.colEnd
            # deleting captured piece
            del dictTurnUpdates[not white][move.capturedPiece]
        elif move.promotion:  # for a promotion move
            # deleting old presenting of selected piece
            del dictTurnUpdates[white][move.selectedPiece[0] + "p" + move.selectedPiece[-1]]
            # adding new presenting
            dictTurnUpdates[white][move.selectedPiece] = move.rowEnd, move.colEnd
        else:  # for a regular move
            # updating selected piece
            dictTurnUpdates[white][move.selectedPiece] = move.rowEnd, move.colEnd
            # updating captured piece of needed
            if move.capturedPiece in dictTurnUpdates[not white].keys():
                del dictTurnUpdates[not white][move.capturedPiece]
            # update captured piece castle state if needed
            if move.capturedPiece in self.Castle and self.Castle[move.capturedPiece]:
                self.dictCastleLog[move.moveID] = self.Castle.copy()
                self.Castle[move.capturedPiece] = False
            # update selected piece castle state if needed
            if move.selectedPiece in self.Castle and self.Castle[move.selectedPiece]:
                self.dictCastleLog[move.moveID] = self.Castle.copy()
                self.Castle[move.selectedPiece] = False

    def undoMove(self, check=False):
        """
        resetting board to last move
        """
        if len(self.moveLog) > 0:  # there is a move to undo
            move = self.moveLog[-1]  # last move in the array
            # restoring board
            self.restoreBoard(move)
            # restoring pieces of needed
            if not check:
                self.restorePieces(move, self.whiteTurn)
            # updating settings
            self.whiteTurn = not self.whiteTurn
            self.moveLog = np.delete(self.moveLog, len(self.moveLog) - 1)

    def restoreBoard(self, move):
        """
        restoring board state according to move annotation, after a move is undo
        :param move: a Move type object
        :return: None
        """
        if move.castling:  # for a castling move
            # updating king position on board
            self.board[move.rowStart][move.colStart] = move.selectedPiece
            self.board[move.rowEnd][move.colEnd] = "---"
            # updating rook position on board
            if move.colEnd < move.colStart:  # left side castling
                self.board[move.rowStart][0] = move.capturedPiece
                self.board[move.rowEnd][move.colEnd + 1] = "---"
            else:  # eight side castling
                self.board[move.rowStart][7] = move.capturedPiece
                self.board[move.rowEnd][move.colEnd - 1] = "---"
        elif move.enPassant:  # for an en-passant move
            # updating selected and captured positions on board
            self.board[move.rowEnd][move.colEnd] = "---"
            self.board[move.rowStart][move.colEnd] = move.capturedPiece
            self.board[move.rowStart][move.colStart] = move.selectedPiece
        elif move.promotion:  # for a promotion move
            # updating piece on board
            move.selectedPiece = move.selectedPiece[0] + "p" + move.selectedPiece[-1]
            self.board[move.rowStart][move.colStart] = move.selectedPiece
            self.board[move.rowEnd][move.colEnd] = "---"
        else:  # for a regular move
            # updating board
            self.board[move.rowEnd][move.colEnd] = move.capturedPiece
            self.board[move.rowStart][move.colStart] = move.selectedPiece

    def restorePieces(self, move, white):
        """
        restoring pieces dictionaries according to move annotation, after a move is undo
        :param move: Move type object
        :param white: boolean type obj. True iff it's a white piece move
        :return: None
        """
        # boolean to color dictionary
        dictTurnUpdates = {True: self.whitePieces, False: self.blackPieces}
        if move.castling:  # for a castling move
            # updating king in dictionary
            dictTurnUpdates[not white][move.selectedPiece] = move.rowStart, move.colStart
            # updating rook in dictionary
            if move.colEnd < move.colStart:  # left side castling
                dictTurnUpdates[not white][move.capturedPiece] = move.rowStart, 0
            else:  # right side castling
                dictTurnUpdates[not white][move.capturedPiece] = move.rowStart, 7
            # updating castle state
            self.Castle = self.dictCastleLog[move.moveID]
            del self.dictCastleLog[move.moveID]
        elif move.enPassant:  # for an en-passant move
            # updating selected piece and captured piece
            dictTurnUpdates[not white][move.selectedPiece] = move.rowStart, move.colStart
            dictTurnUpdates[white][move.capturedPiece] = move.rowEnd, move.colStart
        elif move.promotion:  # for a promotion move
            # deleting old presenting of selected piece
            del dictTurnUpdates[not white][move.selectedPiece[0] + "pq" + move.selectedPiece[-1]]
            # updating new presenting of selected piece
            dictTurnUpdates[not white][move.selectedPiece] = move.rowStart, move.colStart
        else:  # for a regular move
            # updating selected piece
            dictTurnUpdates[not white][move.selectedPiece] = move.rowStart, move.colStart
            # updating captured piece if needed
            if move.capturedPiece != "---":
                dictTurnUpdates[white][move.capturedPiece] = move.rowEnd, move.colEnd
            # updating castling state if needed
            if move.moveID in self.dictCastleLog:
                self.Castle = self.dictCastleLog[move.moveID]
                del self.dictCastleLog[move.moveID]

    def getValidMoves(self):
        """
        computing all valid games on board
        :return: an array of all possible valid move on board
        """
        whitePiecesToFunc = {"wp": self.legalPawnMoves, "wr": self.legalRookMoves, "wk": self.legalKnightMoves,
                             "wb": self.legalBishopMoves, "wq": self.legalQueenMoves, "wK": self.legalKingMoves}
        blackPiecesToFunc = {"bp": self.legalPawnMoves, "br": self.legalRookMoves, "bk": self.legalKnightMoves,
                             "bb": self.legalBishopMoves, "bq": self.legalQueenMoves, "bK": self.legalKingMoves}
        validMoves = np.array([])  # an empty array
        rul = Rules()  # an object for re-checking if a move is valid etc. king is on check
        if self.whiteTurn:  # computing all white pieces moves
            for piece, pos in self.whitePieces.items():  # for every piece from whites
                if piece[:2] == "wp":  # if piece is a pawn we want to send the move-log as another input
                    validMoves = np.concatenate((validMoves, whitePiecesToFunc[piece[:2]](pos, True, self.moveLog)))
                else:
                    validMoves = np.concatenate((validMoves, whitePiecesToFunc[piece[:2]](pos)))
            # validation check
            for move in validMoves:
                self.makeMove(move, True)  # apply move
                if rul.isCheck(self.board, self.whitePieces["wK"], True):  # check for validation
                    validMoves = np.delete(validMoves, np.where(validMoves == move))  # is not valid, delete
                self.undoMove(True)  # undo move
        else:  # same as the above, this time for a black piece move
            for piece, pos in self.blackPieces.items():
                if piece[:2] == "bp":
                    validMoves = np.concatenate((validMoves, blackPiecesToFunc[piece[:2]](pos, False, self.moveLog)))
                else:
                    validMoves = np.concatenate((validMoves, blackPiecesToFunc[piece[:2]](pos, False)))
            for move in validMoves:
                self.makeMove(move, True)
                if rul.isCheck(self.board, self.blackPieces["bK"], False):
                    validMoves = np.delete(validMoves, np.where(validMoves == move))
                self.undoMove(True)
        return validMoves

    def legalPawnMoves(self, piece, white=True, moveLog=None):
        """
        func. computes all valid moves of a certain pawn
        :param moveLog: array of all last moves
        :param piece: pawn position tuple on board
        :param white: is boolean type for a white's turn or black
        :return: validMoves after insertion of all valid moves for piece pawn
        """
        validMoves = np.array([])
        row, col = piece[0], piece[1]  # saving pawn position
        if white:  # white's position
            if row - 1 >= 0:  # if it can move forward
                if self.board[row - 1][col] == "---":  # position one ahead is empty
                    newMove = Move((row, col), (row - 1, col), self.board)  # create move
                    validMoves = np.append(validMoves, np.array([newMove]))  # insert move
                    # pawn at initial position and two ahead is empty
                    if row == 6 and self.board[row - 2][col] == "---":
                        newMove = Move((row, col), (row - 2, col), self.board)
                        validMoves = np.append(validMoves, np.array([newMove]))
                if 0 <= col - 1 and self.board[row - 1][col - 1][0] == "b":  # diagonal from left is with a black piece
                    newMove = Move((row, col), (row - 1, col - 1), self.board)
                    validMoves = np.append(validMoves, np.array([newMove]))
                if col + 1 <= 7 and self.board[row - 1][col + 1][0] == "b":  # diagonal from right is with a black piece
                    newMove = Move((row, col), (row - 1, col + 1), self.board)
                    validMoves = np.append(validMoves, np.array([newMove]))
                if row == 3:
                    # all 6 next lines refer to en Passant move
                    lastMove = moveLog[-1]
                    opt1 = 1 * (col + 1) + 10 * row + 100 * (col + 1) + 1000 * (row - 2)
                    opt2 = 1 * (col - 1) + 10 * row + 100 * (col - 1) + 1000 * (row - 2)
                    if lastMove.selectedPiece[:2] == "bp" and lastMove.moveID == opt1 and col + 1 <= 7:
                        newMove = Move((row, col), (row - 1, col + 1), self.board, True)
                        validMoves = np.append(validMoves, np.array([newMove]))
                    if lastMove.selectedPiece[:2] == "bp" and lastMove.moveID == opt2 and col - 1 >= 0:
                        newMove = Move((row, col), (row - 1, col - 1), self.board, True)
                        validMoves = np.append(validMoves, np.array([newMove]))

        else:  # it is a black move turn
            if row + 1 <= 7:  # can move forward
                if self.board[row + 1][col] == "---":  # on ahead is empty
                    newMove = Move((row, col), (row + 1, col), self.board)  # create move
                    validMoves = np.append(validMoves, np.array([newMove]))  # insert move
                    if row == 1 and self.board[row + 2][col] == "---":  # pawn os on initial position two ahead is empty
                        newMove = Move((row, col), (row + 2, col), self.board)
                        validMoves = np.append(validMoves, np.array([newMove]))
                if 0 <= col - 1 and self.board[row + 1][col - 1][0] == "w":  # diagonal from right is with a white piece
                    newMove = Move((row, col), (row + 1, col - 1), self.board)
                    validMoves = np.append(validMoves, np.array([newMove]))
                if col + 1 <= 7 and self.board[row + 1][col + 1][0] == "w":  # diagonal from left is with a white piece
                    newMove = Move((row, col), (row + 1, col + 1), self.board)
                    validMoves = np.append(validMoves, np.array([newMove]))
                if row == 4:
                    # all 6 next line refer to en Passant move
                    lastMove = moveLog[-1]
                    opt1 = 1 * (col + 1) + 10 * row + 100 * (col + 1) + 1000 * (row + 2)
                    opt2 = 1 * (col - 1) + 10 * row + 100 * (col - 1) + 1000 * (row + 2)
                    if lastMove.selectedPiece[:2] == "wp" and lastMove.moveID == opt1 and col + 1 <= 7:
                        newMove = Move((row, col), (row + 1, col + 1), self.board, True)
                        validMoves = np.append(validMoves, np.array([newMove]))
                    if lastMove.selectedPiece[:2] == "wp" and lastMove.moveID == opt2 and col - 1 >= 0:
                        newMove = Move((row, col), (row + 1, col - 1), self.board, True)
                        validMoves = np.append(validMoves, np.array([newMove]))
        return validMoves

    def legalRookMoves(self, piece, white=True):
        """
        computing all legal moves for a rook piece in the board
        :param piece: position tuple
        :param white: boolean type, true iff it is a white move turn
        :return: validMoves after insertions
        """
        validMoves = np.array([])
        row, col = piece[0], piece[1]  # saving position
        dirDict = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}  # dictionary of all possible directions for a rook
        # (1, 0) = up, (-1, 0) = down, (0, 1) = right, (0, -1) = left
        for i in range(4):  # for every direction do...
            r, c = dirDict[i]  # picking dir
            ind = 1
            while 0 <= row + r * ind <= 7 and 0 <= col + c * ind <= 7:  # if position ahead is inside board
                curPiece = self.board[row + r * ind][col + c * ind]  # picking piece in that position
                if curPiece == "---":  # if it is un captured
                    # create move and insert it
                    newMove = Move((row, col), (row + r * ind, col + c * ind), self.board)
                    validMoves = np.append(validMoves, np.array([newMove]))
                else:  # is captured by some piece
                    # it is a white turn and the currPiece is white, or the same for black piece
                    if (white and curPiece[0] == "b") or (not white and curPiece[0] == "w"):
                        newMove = Move((row, col), (row + r * ind, col + c * ind), self.board)
                        validMoves = np.append(validMoves, np.array([newMove]))
                    break
                ind += 1
        return validMoves

    def legalKnightMoves(self, piece, white=True):
        """
        computing all legal moves for a knight piece in the board
        :param piece: position tuple
        :param white: boolean type, true iff it is a white move turn
        :return: validMoves after insertions
        """
        validMoves = np.array([])
        row, col = piece[0], piece[1]  # saving position
        # all ahead steps for a knight
        knightMoves = {1: (1, 2), 2: (2, 1), 3: (1, -2), 4: (2, -1), 5: (-1, -2), 6: (-2, -1), 7: (-1, 2), 8: (-2, 1)}
        for i in range(1, 9):  # iterate for every step in dictionary
            r, c = knightMoves[i]  # saving steps
            if 0 <= row + r <= 7 and 0 <= col + c <= 7:  # if ahead position is inside board
                curPiece = self.board[row + r][col + c]  # picking piece in that position
                # checking for a possible next position for a knight
                if (white and curPiece[0] != "w") or (not white and curPiece[0] != "b"):
                    newMove = Move((row, col), (row + r, col + c), self.board)
                    validMoves = np.append(validMoves, np.array([newMove]))
        return validMoves

    def legalBishopMoves(self, piece, white=True):
        """
        computing all legal moves for a bishop piece in the board
        :param piece: position tuple
        :param white: boolean type, true iff it is a white move turn
        :return: validMoves after insertions
        """
        validMoves = np.array([])
        row, col = piece[0], piece[1]
        dirDict = {0: (1, 1), 1: (1, -1), 2: (-1, 1), 3: (-1, -1)}
        for i in dirDict.keys():
            r, c = dirDict[i]
            ind = 1
            while 0 <= row + r * ind <= 7 and 0 <= col + c * ind <= 7:
                currPos = self.board[row + r * ind][col + c * ind]
                if currPos == "---":
                    newMove = Move((row, col), (row + r * ind, col + c * ind), self.board)
                    validMoves = np.append(validMoves, np.array([newMove]))
                else:
                    if (white and currPos[0] == "b") or (not white and currPos[0] == "w"):
                        newMove = Move((row, col), (row + r * ind, col + c * ind), self.board)
                        validMoves = np.append(validMoves, np.array([newMove]))
                    break
                ind += 1
        return validMoves

    def legalQueenMoves(self, piece, white=True):
        """
        computing all legal moves for a queen piece in the board
        :param piece: position tuple
        :param white: boolean type, true iff it is a white move turn
        :return: validMoves after insertions
        """
        validMoves = np.concatenate((self.legalBishopMoves(piece, white),
                                     self.legalRookMoves(piece, white)))
        return validMoves

    def legalKingMoves(self, piece, white=True):
        """
        computing all legal moves for a rook piece in the board
        :param piece: position tuple
        :param white: boolean type, true iff it is a white move turn
        :return: validMoves after insertions
        """
        validMoves = np.array([])
        row, col = piece[0], piece[1]
        kingMoves = {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (-1, 1), 4: (-1, 0), 5: (-1, -1), 6: (0, -1), 7: (1, -1)}
        for i in range(8):
            r, c = kingMoves[i]
            if 0 <= row + r <= 7 and 0 <= col + c <= 7:
                currPos = self.board[row + r][col + c]
                if (white and currPos[0] != "w") or (not white and currPos[0] != "b"):
                    newMove = Move((row, col), (row + r, col + c), self.board)
                    validMoves = np.append(validMoves, np.array([newMove]))
        # castling
        if self.Castle[self.board[row][col]]:
            dictBooleanColors = {True: "w", False: "b"}
            for i in range(1, 3):
                rook = dictBooleanColors[white] + "r" + str(i)
                if self.Castle[rook]:
                    if self.isLegalCastle(rook, white):
                        if i == 1:
                            newMove = Move((row, col), (row, col - 2), self.board, False, True)
                        else:
                            newMove = Move((row, col), (row, col + 2), self.board, False, True)
                        validMoves = np.append(validMoves, np.array([newMove]))
        return validMoves

    def isLegalCastle(self, rook, white=True):
        rul = Rules()
        if (white and rul.isCheck(self.board, self.whitePieces["wK"], True)) or \
                (not white and rul.isCheck(self.board, self.blackPieces["bK"], False)):
            return False
        for i in range(min(3, (int(rook[2]) // 2) * 7) + 1, max(3, (int(rook[2]) // 2) * 7)):
            if self.board[int(white) * 7][i] != "---":
                return False
        return True


class Move:
    """
    this class responsible for evaluating move and generating move annotations and valid moves
    """
    # form dictionaries: from annotations to position and the opposite way
    rankToRow = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowToRank = {v: k for k, v in rankToRow.items()}
    rankToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colToRank = {v: k for k, v in rankToCol.items()}

    # initial a new move
    def __init__(self, startLoc, endLoc, board, enPassant=False, castling=False):
        # where from
        self.rowStart = startLoc[0]
        self.colStart = startLoc[1]
        # where to
        self.rowEnd = endLoc[0]
        self.colEnd = endLoc[1]
        # if move is en Passant type
        if self.isEnPassant(board) or enPassant:
            self.enPassant = True
        else:
            self.enPassant = False
        # if move is a castle move type
        if self.isCastling(board) or castling:
            self.castling = True
        else:
            self.castling = False
        # if move is a promotion move type
        if self.isPromotion(self.rowEnd, self.colStart, self.colEnd, board[self.rowStart][self.colStart]):
            self.promotion = True
        else:
            self.promotion = False
        # pieces involved
        self.selectedPiece = board[self.rowStart][self.colStart]
        if self.enPassant or self.promotion:
            self.capturedPiece = board[self.rowStart][self.colEnd]
        elif self.castling:
            if self.colStart < self.colEnd:
                self.capturedPiece = board[self.rowStart][7]
            else:
                self.capturedPiece = board[self.rowStart][0]
        elif self.promotion:
            pass
        else:
            self.capturedPiece = board[self.rowEnd][self.colEnd]
        self.moveID = 1000000 * self.promotion + 100000 * self.castling + 10000 * self.enPassant + \
                      1000 * self.rowStart + 100 * self.colStart + 10 * self.rowEnd + 1 * self.colEnd

    def isEnPassant(self, board):
        if self.rowStart == 3:
            if board[self.rowStart][self.colStart][:2] == "wp":
                if board[self.rowEnd][self.colEnd] == "---":
                    if board[self.rowStart][self.colEnd][:2] == "bp":
                        return True
        elif self.rowStart == 4:
            if board[self.rowStart][self.colStart][:2] == "bp":
                if board[self.rowEnd][self.colEnd] == "---":
                    if board[self.rowStart][self.colEnd][:2] == "wp":
                        return True
        return False

    def isCastling(self, board):
        if board[self.rowStart][self.colStart][1] == "K":
            if self.colStart == 3 and np.abs(self.colEnd - self.colStart) == 2:
                return True
        return False

    @staticmethod
    def isPromotion(rowEnd, colStart, colEnd, piece):
        if piece[:2] == "wp" and rowEnd == 0 and colStart == colEnd:
            return True
        elif piece[:2] == "bp" and rowEnd == 7 and colStart == colEnd:
            return True
        return False

    def __eq__(self, other):
        """
        checking for equivalence with another move
        :param other: a move type object
        :return:
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID  # checking if both ids are equal

    def getChessNotation(self):  # saving the move notation
        return self.getRankStr(self.rowStart, self.colStart) + self.getRankStr(self.rowEnd, self.colEnd)

    def getRankStr(self, row, col):
        return self.colToRank[col] + self.rowToRank[row]


class Rules:
    """
    this class response for checking if a move is valid,
    etc. the king is on check and so on
    """
    """
        checking whether the king is on threat
    """

    def isCheck(self, board, kingPos, white=True):
        return self.isInThreat(board, kingPos, white)

    def isInThreat(self, board, piece, white=True):
        """
        :param board: current board status
        :param piece: piece to be checked, a tuple of 2 integers represents the place on the board
        :param white: a boolean to check whether black is threaten by or white is
        :return: boolean obj. True iff is on threat
        """
        # checking if there is a threat on the diagonals
        posDiagonals = self.diagonals(board, piece, white)
        # checking if there is a threat on the vertical
        posVertices = self.vertices(board, piece, white)
        # checking if there is a threat from a knight
        posKnightMoves = self.KnightMoves(board, piece, white)
        return posVertices or posDiagonals or posKnightMoves

    """
    all 9 next functions are checking if when given a certain piece and color, 
    that piece is threaten by the opposite player pieces from diagonal, vertical, horizon or a knight
    """

    @staticmethod
    def KnightMoves(board, piece, white):
        """
        functions will check if a piece is being threat from an opposite knight
        :param board: board game status
        :param piece: piece to ce checked
        :param white: is a white piece or not
        :return: true iff piece is under threat from a knight
        """
        row, col = piece[0], piece[1]  # saving positions
        # two sets of white and black knights
        whiteKnights = {"wk1", "wk2"}
        blackKnights = {"bk1", "bk2"}
        knightAhead = set()  # set of all pieces ahead from piece pos, moved as like a knight
        knightTupleInd = {(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)}  # all knight moves
        for tup in knightTupleInd:
            if (0 <= row + tup[0] <= 7) and (0 <= col + tup[1] <= 7):  # if a move is inside board limits
                currPos = board[row + tup[0]][col + tup[1]]  # catch piece in that position
                set.add(knightAhead, currPos)  # insert piece to the set
        # seeing if there is a match between black knight and moves a head or opposite
        if white and len(knightAhead.intersection(blackKnights)) > 0:
            return True
        elif not white and len(knightAhead.intersection(whiteKnights)) > 0:
            return True
        return False

    @staticmethod
    def vertices(board, piece, white=True):
        """
        functions will check if a piece is being threat from an opposite queen, rook or a King if can
        :param board: board game status
        :param piece: piece to ce checked
        :param white: is a white piece or not
        :return: true iff piece is under threat from a queen, rook or a King if can
        """
        row, col = piece[0], piece[1]  # saving row and col
        dirDict = {0: (1, 0), 1: (0, -1), 2: (-1, 0), 3: (0, 1)}  # directions dictionary
        for i in range(4):  # for every direction
            r, c = dirDict[i]
            ind = 1  # distance from row and col
            while 0 <= row + r * ind <= 7 and 0 <= col + c * ind <= 7:  # as long position ahead is in board limits
                currPos = board[row + r * ind][col + c * ind]  # curr piece in that position
                if currPos == "---":  # if no piece in that position
                    ind += 1
                    continue
                # if piece can threaten on row,col position
                elif white and currPos[:2] in {"br", "bq", "bK"}:
                    return True
                elif not white and currPos[:2] in {"wr", "wq", "wK"}:
                    return True
                else:  # piece is not blanked and can't make a threat
                    break
        return False

    @staticmethod
    def diagonals(board, piece, white=True):
        """
        functions will check if a piece is being threat from an opposite queen, bishop or a King/pawn if can
        :param board: board game status
        :param piece: piece to ce checked
        :param white: is a white piece or not
        :return: true iff piece is under threat from a queen, bishop or a King/pawn if can
        """
        row, col = piece[0], piece[1]
        dirDict = {0: (1, 1), 1: (-1, 1), 2: (-1, -1), 3: (1, -1)}
        for i in range(4):
            r, c = dirDict[i]
            ind = 1
            while 0 <= row + r * ind <= 7 and 0 <= col + c * ind <= 7:
                currPos = board[row + r * ind][col + c * ind]
                if currPos == "---":
                    ind += 1
                    continue
                if white and currPos[:2] == "bp":
                    if r < 0 and ind == 1:
                        return True
                    ind += 1
                elif white and currPos[:2] in {"bb", "bq", "bK"}:
                    return True
                elif not white and currPos[:2] == "wp":
                    if r > 0 and ind == 1:
                        return True
                    ind += 1
                elif not white and currPos[:2] in {"wb", "wq", "wK"}:
                    return True
                else:
                    break
        return False
