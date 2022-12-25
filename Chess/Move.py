import numpy as np

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
    def __init__(self, startLoc: tuple, endLoc: tuple, board: np.ndarray, enPassant=False, castling=False) -> None:
        # where from
        self.rowStart = startLoc[0]
        self.colStart = startLoc[1]
        # where to
        self.rowEnd = endLoc[0]
        self.colEnd = endLoc[1]
        # if move is en Passant type
        if self.isEnPassant(board=board) or enPassant:
            self.enPassant = True
        else:
            self.enPassant = False
        # if move is a castle move type
        if self.isCastling(board=board) or castling:
            self.castling = True
        else:
            self.castling = False
        # if move is a promotion move type
        if self.isPromotion(rowEnd=self.rowEnd, colStart=self.colStart, colEnd=self.colEnd,
                            piece=board[self.rowStart][self.colStart]):
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



    def isEnPassant(self, board: np.ndarray) -> bool:
        try:
            if self.rowStart == 3:
                if board[self.rowStart][self.colStart].isWhitePawn():
                    if board[self.rowEnd][self.colEnd] is None:
                        if board[self.rowStart][self.colEnd].isBlackPawn():
                            return True
            elif self.rowStart == 4:
                if board[self.rowStart][self.colStart].isBlackPawn():
                    if board[self.rowEnd][self.colEnd] is None:
                        if board[self.rowStart][self.colEnd].isWhitePawn():
                            return True
        except AttributeError:
            pass
        return False

    def isCastling(self, board: np.ndarray) -> bool:
        from Chess.ChessPieces.Rook import Rook
        try:
            if board[self.rowStart][self.colStart].isWhiteKing() and self.rowEnd == self.rowStart == 7:
                if self.colEnd == self.colStart - 2:
                    piece = board[self.rowStart][0]
                    if isinstance(piece, Rook) and piece.white:
                        for i in range(1, 3):
                            if board[self.rowEnd][i] is not None:
                                return False
                        return True
                elif self.colEnd == self.colStart + 2:
                    piece = board[self.rowStart][7]
                    if isinstance(piece, Rook) and piece.white:
                        for i in range(4, 7):
                            if board[self.rowEnd][i] is not None:
                                return False
                        return True
            elif board[self.rowStart][self.colStart].name == "bX" and self.rowEnd == self.rowStart == 0:
                if self.colEnd == self.colStart - 2:
                    piece = board[self.rowStart][0]
                    if isinstance(piece, Rook) and not piece.white:
                        for i in range(1, 3):
                            if board[self.rowEnd][i] is not None:
                                return False
                        return True
                elif self.colEnd == self.colStart + 2:
                    piece = board[self.rowStart][7]
                    if isinstance(piece, Rook) and not piece.white:
                        for i in range(4, 7):
                            if board[self.rowEnd][i] is not None:
                                return False
                        return True
        except AttributeError:
            pass
        return False

    @staticmethod
    def isPromotion(rowEnd: int, colStart: int, colEnd: int, piece=None) -> bool:
        try:
            if piece.isWhitePawn() and rowEnd == 0 and colStart == colEnd:
                return True
            elif piece.isBlackPawn() and rowEnd == 7 and colStart == colEnd:
                return True
        except AttributeError:
            pass
        return False

    def __eq__(self, other: object) -> bool:
        """
        checking for equivalence with another move
        :param other: a move type object
        :return:
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID  # checking if both ids are equal

    def getChessNotation(self) -> str:  # saving the move notation
        return self.getRankStr(row=self.rowStart, col=self.colStart) + self.getRankStr(row=self.rowEnd, col=self.colEnd)

    def getRankStr(self, row: int, col: int) -> str:
        return self.colToRank[col] + self.rowToRank[row]
