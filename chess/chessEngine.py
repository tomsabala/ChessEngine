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
        # black and white pieces' dictionary for positions etc. uses to eval game state
        self.blackPieces = {"br1": (0, 0), "bk1": (0, 1), "bb1": (0, 2), "bK": (0, 3), "bq": (0, 4), "bb2": (0, 5),
                            "bk2": (0, 6), "br2": (0, 7), "bp1": (1, 0), "bp2": (1, 1), "bp3": (1, 2), "bp4": (1, 3),
                            "bp5": (1, 4), "bp6": (1, 5), "bp7": (1, 6), "bp8": (1, 7)}
        self.whitePieces = {"wr1": (7, 0), "wk1": (7, 1), "wb1": (7, 2), "wK": (7, 3), "wq": (7, 4), "wb2": (7, 5),
                            "wk2": (7, 6), "wr2": (7, 7), "wp1": (6, 0), "wp2": (6, 1), "wp3": (6, 2), "wp4": (6, 3),
                            "wp5": (6, 4), "wp6": (6, 5), "wp7": (6, 6), "wp8": (6, 7)}
        self.whiteTurn = True  # a boolean obj. for whose turn is it
        self.moveLog = np.array([])  # an array of all moves

    def makeMove(self, move):
        """
        initial move as a play on the board
        """
        if move.castling:  # for a castling type move
            pass
        elif move.enPassant:  # for enPassant type move
            # updating board state
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece
            self.board[move.rowStart][move.colStart] = "---"
            self.board[move.rowStart][move.colEnd] = "---"
            # updating white and black pieces dictionary
            if self.whiteTurn:
                self.whitePieces[move.selectedPiece] = move.rowEnd, move.colEnd
                del self.blackPieces[move.capturedPiece]
            else:
                self.blackPieces[move.selectedPiece] = move.rowEnd, move.colEnd
                del self.whitePieces[move.capturedPiece]
        else:  # for a regular type move
            self.board[move.rowStart][move.colStart] = "---"  # last position becomes empty
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece  # selected piece moving to the next position
            if self.whiteTurn:
                self.whitePieces[move.selectedPiece] = move.rowEnd, move.colEnd
                if move.capturedPiece in self.blackPieces.keys():
                    del self.blackPieces[move.capturedPiece]
            else:
                self.blackPieces[move.selectedPiece] = move.rowEnd, move.colEnd
                if move.capturedPiece in self.whitePieces.keys():
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
            elif move.enPassant:  # for a enPassant type move
                # updating board state
                self.board[move.rowEnd][move.colEnd] = "---"
                self.board[move.rowStart][move.colStart] = move.selectedPiece
                self.board[move.rowStart][move.colEnd] = move.capturedPiece
                # updating white and black pieces
                if not self.whiteTurn:
                    self.blackPieces[move.capturedPiece] = move.rowEnd, move.colStart
                    self.whitePieces[move.selectedPiece] = move.rowStart, move.colStart
                else:
                    self.whitePieces[move.capturedPiece] = move.rowEnd, move.colStart
                    self.blackPieces[move.selectedPiece] = move.rowStart, move.colStart
            else:  # for a regular type move
                # updating board
                self.board[move.rowEnd][move.colEnd] = move.capturedPiece
                self.board[move.rowStart][move.colStart] = move.selectedPiece
                # updating white and black pieces
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
            # updating settings
            self.whiteTurn = not self.whiteTurn
            self.moveLog = np.delete(self.moveLog, len(self.moveLog) - 1)

    def getValidMoves(self):
        """
        computing all valid games on board
        :return: an array of all possible valid move on board
        """
        validPawnMove = np.array([])  # an empty array
        rul = Rules(self.board)  # an object for re-checking if a move is valid etc. king is on check
        if self.whiteTurn:  # computing all white pieces moves
            for piece, pos in self.whitePieces.items():  # for every piece from whites
                if piece[:2] == "wp":  # refer to a white pawn type
                    validPawnMove = self.legalPawnMoves(self.board, pos, validPawnMove)  # getting all pawn moves
            # validation check
            for move in validPawnMove:
                self.makeMove(move)  # apply move
                if rul.isCheck(self.board, self.whitePieces["wK"], True):  # check for validation
                    validPawnMove = validPawnMove.__delitem__(move)  # is not valid, delete
                self.undoMove()  # undo move
        else:  # same as the above, this time for a black piece move
            for piece, pos in self.blackPieces.items():
                if piece[:2] == "bp":
                    validPawnMove = self.legalPawnMoves(self.board, pos, validPawnMove, False)
            for move in validPawnMove:
                self.makeMove(move)
                if rul.isCheck(self.board, self.blackPieces["bK"], False):
                    validPawnMove = validPawnMove.__delitem__(move)
                self.undoMove()
        return validPawnMove

    def legalPawnMoves(self, board, piece, validMoves, white=True):
        """
        func. computes all valid moves of a certain pawn
        :param board: board state, etc. pieces and positions
        :param piece: pawn position tuple on board
        :param validMoves: an array of all valid moves to insert in
        :param white: is boolean type for a white's turn or black
        :return: validMoves after insertion of all valid moves for piece pawn
        """
        row, col = piece[0], piece[1]  # saving pawn position
        if white:  # white's position
            if row - 1 >= 0:  # if it can move forward
                if board[row - 1][col] == "---":  # position one ahead is empty
                    newMove = Move((row, col), (row - 1, col), board)  # create move
                    validMoves = np.append(validMoves, newMove)  # insert move
                    if row == 6 and board[row - 2][col] == "---":  # pawn at initial position and two ahead is empty
                        newMove = Move((row, col), (row - 2, col), board)
                        validMoves = np.append(validMoves, newMove)
                if 0 <= col - 1 and board[row - 1][col - 1][0] == "b":  # diagonal from left is with a black piece
                    newMove = Move((row, col), (row - 1, col - 1), board)
                    validMoves = np.append(validMoves, newMove)
                if col + 1 <= 7 and board[row - 1][col + 1][0] == "b":  # diagonal from right is with a black piece
                    newMove = Move((row, col), (row - 1, col + 1), board)
                    validMoves = np.append(validMoves, newMove)
                if row == 3:
                    # all 6 next lines refer to en Passant move
                    if col - 1 >= 0 and board[row][col - 1][:2] == "bp":
                        newMove = Move((row, col), (row - 1, col - 1), board, True)
                        validMoves = np.append(validMoves, newMove)
                    if col + 1 <= 7 and board[row][col + 1][:2] == "bp":
                        newMove = Move((row, col), (row - 1, col + 1), board, True)
                        validMoves = np.append(validMoves, newMove)
        else:  # it is a black move turn
            if row + 1 <= 7:  # can move forward
                if board[row + 1][col] == "---":  # on ahead is empty
                    newMove = Move((row, col), (row + 1, col), board)  # create move
                    validMoves = np.append(validMoves, newMove)  # insert move
                    if row == 1 and board[row + 2][col] == "---":  # pawn os on initial position two ahead is empty
                        newMove = Move((row, col), (row + 2, col), board)
                        validMoves = np.append(validMoves, newMove)
                if 0 <= col - 1 and board[row + 1][col - 1][0] == "w":  # diagonal from right is with a white piece
                    newMove = Move((row, col), (row + 1, col - 1), board)
                    validMoves = np.append(validMoves, newMove)
                if col + 1 <= 7 and board[row + 1][col + 1][0] == "w":  # diagonal from left is with a white piece
                    newMove = Move((row, col), (row + 1, col + 1), board)
                    validMoves = np.append(validMoves, newMove)
                if row == 4:
                    # all 6 next line refer to en Passant move
                    if col - 1 >= 0 and board[row][col - 1][:2] == "wp":
                        newMove = Move((row, col), (row + 1, col - 1), board, True)
                        validMoves = np.append(validMoves, newMove)
                    if col + 1 <= 7 and board[row][col + 1][:2] == "wp":
                        newMove = Move((row, col), (row + 1, col + 1), board, True)
                        validMoves = np.append(validMoves, newMove)
        return validMoves

    def legalRookMoves(self, board, piece, validMoves, white=True):
        pass

    def legalKnightMoves(self, board, piece, validMoves, white=True):
        pass

    def legalBishopMoves(self, board, piece, validMoves, white=True):
        pass

    def legalQueenMoves(self, board, piece, validMoves, white=True):
        pass

    def legalKingMoves(self, board, piece, validMoves, white=True):
        pass


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

    def __init__(self, board):
        self.board = board

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
        posDiagonal = self.downRightDiagonal(board, piece, white) or self.downLeftDiagonal(board, piece, white) or self\
            .upLeftDiagonal(board, piece, white) or self.upRightDiagonal(board, piece, white)
        # checking if there is a threat on the vertical
        posVertical = self.verticalUp(board, piece, white) or self.verticalDown(board, piece, white)
        # checking if there is a threat on the horizon
        posHorizon = self.horizonLeft(board, piece, white) or self.horizonRight(board, piece, white)
        # checking if there is a threat from a knight
        posKnightMoves = self.KnightMoves(board, piece, white)
        return posHorizon or posVertical or posDiagonal or posKnightMoves

    """
    all 9 next functions are checking if when given a certain piece and color, 
    that piece is threaten by the opposite player pieces from diagonal, vertical, horizon or a knight
    """
    def KnightMoves(self, board, piece, white):
        """
        functions will check if a piece is being threat from an opposite knight
        :param board: board state, pieces and positions
        :param piece: piece to ce checked
        :param white: is a white piece or not
        :return: true iff piece is under threat from a knight
        """
        row, col = piece[0], piece[1]  # saving positions
        # two sets of white and black knights
        whiteKnights = {"wk1", "wk2"}
        blackKnights = {"bk1", "bk2"}
        knightAhead = set()  # set of all pieces ahead from piece pos, moved as like a knight
        knightTuppleInd = {(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)}  # all knight moves
        for tup in knightTuppleInd:
            if (0 <= row + tup[0] <= 7) and (0 <= col + tup[1] <= 7):  # if a move is inside board limits
                currPos = board[row + tup[0]][col + tup[1]]  # catch piece in that position
                set.add(knightAhead, currPos)  # insert piece to the set
        # seeing if there is a match between black knight and moves a head or opposite
        if white and len(knightAhead.intersection(blackKnights)) > 0:
            return True
        elif not white and len(knightAhead.intersection(whiteKnights)) > 0:
            return True
        return False

    def downRightDiagonal(self, board, piece, white=True):
        """
            functions will check if a piece is being threat from right down diagonal
            :param board: board state, pieces and positions
            :param piece: piece to ce checked
            :param white: is a white piece or not
            :return: true iff piece is under threat from down right side
        """
        row, col = piece[0], piece[1]  # saving position
        i = 1
        while 0 <= row + i <= 7 and 0 <= col + i <= 7:  # if the position ahead is inside board
            currPos = board[row + i][col + i]  # taking piece from that position ahead
            if white:
                # checking if that currPiece can take on piece
                if currPos in {"bq", "bb1", "bb2"} or (i == 1 and currPos == "bK"):
                    return True
                elif currPos != "---":
                    break
                # same only now for the opposite player
            else:
                if currPos in {"wq", "wb1", "wb2"} or (i == 1 and currPos[:2] in {"wp", "wK"}):
                    return True
                elif currPos != "---":
                    break
            i += 1
        return False

    def downLeftDiagonal(self, board, piece, white=True):
        """
            functions will check if a piece is being threat from left down diagonal
            :param board: board state, pieces and positions
            :param piece: piece to ce checked
            :param white: is a white piece or not
            :return: true iff piece is under threat from down right side
        """
        row, col = piece[0], piece[1]  # saving position
        i = 1
        j = -1
        while 0 <= row + i <= 7 and 0 <= col + j <= 7:  # if position ahead is inside board
            currPos = board[row + i][col + j]  # picking piece in that position
            if white:
                # checking if that currPiece can take on piece
                if currPos in {"bq", "bb1", "bb2"} or (i == 1 and j == -1 and currPos == "bK"):
                    return True
                elif currPos != "---":
                    break
            else:
                # same only now for the opposite player
                if currPos in {"wq", "wb1", "wb2"} or (i == 1 and j == -1 and currPos[:2] in {"wp", "wK"}):
                    return True
                elif currPos != "---":
                    break
            j -= 1
            i += 1
        return False

    def upLeftDiagonal(self, board, piece, white=True):
        """
            functions will check if a piece is being threat from left up diagonal
            :param board: board state, pieces and positions
            :param piece: piece to ce checked
            :param white: is a white piece or not
            :return: true iff piece is under threat from down right side
        """
        row, col = piece[0], piece[1]  # saving position
        i = -1
        while 0 <= row + i <= 7 and 0 <= col + i <= 7:  # if position ahead is inside board
            currPos = board[row + i][col + i]  # picking piece in that position
            if white:
                # checking if that currPiece can take on piece
                if currPos in {"bq", "bb1", "bb2"} or (i == -1 and currPos[:2] in {"bp", "bK"}):
                    return True
                elif currPos != "---":
                    break
            else:
                # same only now for the opposite player
                if currPos in {"wq", "wb1", "wb2"} or (i == -1 and currPos[:2] == "wK"):
                    return True
                elif currPos != "---":
                    break
            i -= 1
        return False

    def upRightDiagonal(self, board, piece, white=True):
        """
            functions will check if a piece is being threat from right up diagonal
            :param board: board state, pieces and positions
            :param piece: piece to ce checked
            :param white: is a white piece or not
            :return: true iff piece is under threat from down right side
        """
        row, col = piece[0], piece[1]  # saving position
        i = -1
        j = 1
        while 0 <= row + i <= 7 and 0 <= col + j <= 7:  # if position ahead is inside board
            currPos = board[row + i][col + j]  # picking piece in that position
            if white:
                # checking if that currPiece can take on piece
                if currPos in {"bq", "bb1", "bb2"} or (i == -1 and j == 1 and currPos[:2] in {"bp", "bK"}):
                    return True
                elif currPos != "---":
                    break
            else:
                # same only now for the opposite player
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

    def verticalDown(self, board, position, white=True, down=1):
        row, col = position[0], position[1]
        i = 1
        while 0 <= row + down * i <= 7:
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
        """
        checking for a threat from vertical up direction
        :param board: board status
        :param position: possible position under threat
        :param white: is position white or not
        :return: true or false
        """
        row, col = position[0], position[1]  # saving position values
        j = -1
        while 0 <= row + j <= 7:  # running on every position
            currPos = board[row + j][col]  # player in curr position
            if white:
                # our position is white, so need to check for a threat from black
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
