from . import Piece
from Chess.ChessPieces.Knight import Knight
from Chess.ChessPieces.Rook import Rook
from Chess.Move import Move
import numpy as np


class King(Piece.Piece):
    def __init__(self, board: np.ndarray, pos: tuple, name: str, white: bool) -> None:
        super(King, self).__init__(board=board, pos=pos, name=name, white=white)

    def getValidMoves(self, castleDict: dict) -> list:
        """
        computing all legal moves for a rook piece in the board
        :return: validMoves after insertions
        """
        validMoves = []
        row, col = self.pos[0], self.pos[1]
        kingMoves = {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (-1, 1), 4: (-1, 0), 5: (-1, -1), 6: (0, -1), 7: (1, -1)}
        for i in range(8):
            r, c = kingMoves[i]
            if 0 <= row + r <= 7 and 0 <= col + c <= 7:
                currPos = self.board[row + r][col + c]
                if currPos is None:
                    newMove = Move(startLoc=(row, col), endLoc=(row + r, col + c), board=self.board)
                    validMoves.append(newMove)
                    continue
                if (self.white and not currPos.white) or (not self.white and currPos.white):
                    newMove = Move(startLoc=(row, col), endLoc=(row + r, col + c), board=self.board)
                    validMoves.append(newMove)
        # castling
        if castleDict[self.board[row][col]]:
            rook_pos = {True: ((7, 0), (7, 7)), False: ((0, 0), (0, 7))}
            for r, c in rook_pos[self.white]:
                rook = self.board[r][c]
                if not isinstance(rook, Rook):
                    continue
                if castleDict[rook]:
                    if self.isLegalCastle(kingPos=(row, col), rook=rook):
                        if c == 0:
                            newMove = Move(startLoc=(row, col), endLoc=(row, col - 2), board=self.board,
                                           enPassant=False, castling=True)
                        else:
                            newMove = Move(startLoc=(row, col), endLoc=(row, col + 2), board=self.board,
                                           enPassant=False, castling=True)
                        validMoves.append(newMove)
        return validMoves

    def isLegalCastle(self, kingPos: tuple, rook: Rook) -> bool:
        dictColorKing = {True: ("wX", 7), False: ("bX", 0)}
        if self.isCheck():
            return False
        if self.board[kingPos[0]][kingPos[1]].name == dictColorKing[self.white][0] and\
                kingPos[0] == dictColorKing[self.white][1]:
            for i in range(min(3, (int(rook.name[2]) // 2) * 7) + 1, max(3, (int(rook.name[2]) // 2) * 7)):
                if self.board[int(self.white) * 7][i] is not None:
                    return False
            return True
        else:
            return False

    def isCheck(self) -> bool:
        return self.isInThreat()

    def isInThreat(self) -> bool:
        """
        :return: boolean obj. True iff is on threat
        """
        # checking if there is a threat on the diagonals
        posDiagonals = self.diagonals()
        # checking if there is a threat on the vertical
        posVertices = self.vertices()
        # checking if there is a threat from a knight
        posKnightMoves = self.KnightMoves()
        return posVertices or posDiagonals or posKnightMoves

    def diagonals(self) -> bool:
        """
        function will check if a piece is being threat from an opposite queen, bishop or a King/pawn if can
        :return: true iff piece is under threat from a queen, bishop or a King/pawn if can
        """
        row, col = self.pos[0], self.pos[1]
        dirDict = {0: (1, 1), 1: (-1, 1), 2: (-1, -1), 3: (1, -1)}
        for i in range(4):
            r, c = dirDict[i]
            ind = 1
            while 0 <= row + r * ind <= 7 and 0 <= col + c * ind <= 7:
                currPos = self.board[row + r * ind][col + c * ind]
                if currPos is None:
                    ind += 1
                    continue
                elif self.white:
                    if currPos.isBlackPawn() and ind == 1 and r < 0:
                        return True
                    elif currPos.isBlackKing() and ind == 1:
                        return True
                    elif currPos.name[:2] in {"bb", "bq"}:
                        return True
                    break
                else:
                    if currPos.isWhitePawn() and ind == 1 and r > 0:
                        return True
                    elif currPos.isWhiteKing() and ind == 1:
                        return True
                    elif currPos.name[:2] in {"wb", "wq"}:
                        return True
                    break
        return False

    def vertices(self) -> bool:
        """
        functions will check if a piece is being threat from an opposite queen, rook or a King if can
        :return: true iff piece is under threat from a queen, rook or a King if can
        """
        row, col = self.pos[0], self.pos[1]  # saving row and col
        dirDict = {0: (1, 0), 1: (0, -1), 2: (-1, 0), 3: (0, 1)}  # directions dictionary
        for i in range(4):  # for every direction
            r, c = dirDict[i]
            ind = 1  # distance from row and col
            while 0 <= row + r * ind <= 7 and 0 <= col + c * ind <= 7:  # as long position ahead is in board limits
                currPos = self.board[row + r * ind][col + c * ind]  # curr piece in that position
                if currPos is None:  # if no piece in that position
                    ind += 1
                    continue
                elif self.white:
                    if currPos.isBlackKing() and ind == 1:
                        return True
                    elif currPos.name[:2] in {"br", "bq"}:
                        return True
                    break
                else:
                    if currPos.isWhiteKing() and ind == 1:
                        return True
                    elif currPos.name[:2] in {"wr", "wq"}:
                        return True
                    break
        return False

    def KnightMoves(self) -> bool:
        """
        functions will check if a piece is being threat from an opposite knight
        :return: true iff piece is under threat from a knight
        """
        row, col = self.pos[0], self.pos[1]  # saving positions
        knightTupleInd = {(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)}  # all knight moves
        for tup in knightTupleInd:
            if (0 <= row + tup[0] <= 7) and (0 <= col + tup[1] <= 7):  # if a move is inside board limits
                currPos = self.board[row + tup[0]][col + tup[1]]  # catch piece in that position
                if isinstance(currPos, Knight) and currPos.white != self.white:
                    return True
        return False


def main(board: np.ndarray, white: bool) -> King:
    color2prop = {True: ("w", 7), False: ("b", 0)}
    king = King(board=board,
                  pos=(color2prop[white][1], 3),
                  name=color2prop[white][0]+"X",
                  white=white)

    board[king.pos[0]][king.pos[1]] = king

    return king
