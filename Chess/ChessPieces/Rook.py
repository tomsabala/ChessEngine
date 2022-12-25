from Chess.Move import Move
from Chess.ChessPieces.Piece import Piece
import numpy as np


class Rook(Piece):
    def __init__(self, board: np.ndarray, pos: tuple, name: str, white: bool) -> None:
        super(Rook, self).__init__(board=board, pos=pos, name=name, white=white)

    def getValidMoves(self) -> list:
        """
            computing all legal moves for a rook piece in the board
            :return: validMoves after insertions
        """
        validMoves = []
        row, col = self.pos  # saving position
        dirDict = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}  # dictionary of all possible directions for a rook
        # (1, 0) = up, (-1, 0) = down, (0, 1) = right, (0, -1) = left
        for i in range(4):  # for every direction do...
            r, c = dirDict[i]  # picking dir
            ind = 1
            while 0 <= row + r * ind <= 7 and 0 <= col + c * ind <= 7:  # if position ahead is inside board
                curPiece = self.board[row + r * ind][col + c * ind]  # picking piece in that position
                if curPiece is None:  # if it is un captured
                    # create move and insert it
                    newMove = Move(startLoc=(row, col), endLoc=(row + r * ind, col + c * ind), board=self.board)
                    validMoves.append(newMove)
                else:  # is captured by some piece
                    # it is a white turn and the currPiece is white, or the same for black piece
                    if (self.white and not curPiece.white) or (not self.white and curPiece.white):
                        newMove = Move(startLoc=(row, col), endLoc=(row + r * ind, col + c * ind), board=self.board)
                        validMoves.append(newMove)
                    break
                ind += 1
        return validMoves

    def makeMove(self, move: Move, isCastle=False) -> None:
        if isCastle:
            if move.colEnd < move.colStart:  # for a left side castling
                self.pos = move.rowEnd, move.colEnd + 1
            else:  # for a right side castling
                self.pos = move.rowEnd, move.colEnd - 1
        else:
            super(Rook, self).makeMove(move=move)

    def undoMove(self, move: Move, isCastle=False) -> None:
        if isCastle:
            if move.colEnd < move.colStart:  # left side castling
                self.pos = move.rowStart, 0
            else:  # eight side castling
                self.pos = move.rowStart, 7
        else:
            super(Rook, self).undoMove(move=move)


def main(board: np.ndarray, white: bool) -> list:
    if white:
        rook1 = Rook(board=board, pos=(7, 0), name="wr1", white=True)
        rook2 = Rook(board=board, pos=(7, 7), name="wr2", white=True)
    else:
        rook1 = Rook(board=board, pos=(0, 0), name="br1", white=False)
        rook2 = Rook(board=board, pos=(0, 7), name="br2", white=False)

    board[rook1.pos[0]][rook1.pos[1]] = rook1
    board[rook2.pos[0]][rook2.pos[1]] = rook2

    return [rook1, rook2]
