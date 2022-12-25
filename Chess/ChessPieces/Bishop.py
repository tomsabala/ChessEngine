from Chess.Move import Move
from Chess.ChessPieces.Piece import Piece
import numpy as np


class Bishop(Piece):
    def __init__(self, board: np.ndarray, pos: tuple, name: str, white: bool) -> None:
        super(Bishop, self).__init__(board=board, pos=pos, name=name, white=white)

    def getValidMoves(self) -> list:
        """
        computing all legal moves for a bishop piece in the board
        :return: validMoves after insertions
        """
        validMoves = []
        row, col = self.pos[0], self.pos[1]
        dirDict = {0: (1, 1), 1: (1, -1), 2: (-1, 1), 3: (-1, -1)}
        for i in range(4):
            r, c = dirDict[i]
            ind = 1
            while 0 <= row + r*ind <= 7 and 0 <= col + c*ind <= 7:
                currPos = self.board[row + r*ind][col + c*ind]
                if currPos is None:
                    newMove = Move(startLoc=(row, col), endLoc=(row + r*ind, col + c*ind), board=self.board)
                    validMoves.append(newMove)
                else:
                    if (self.white and not currPos.white) or (not self.white and currPos.white):
                        newMove = Move(startLoc=(row, col), endLoc=(row + r*ind, col + c*ind), board=self.board)
                        validMoves.append(newMove)
                    break
                ind += 1
        return validMoves


def main(board: np.ndarray, white: bool) -> list:
    if white:
        bishop1 = Bishop(board=board, pos=(7, 2), name="wb1", white=True)
        bishop2 = Bishop(board=board, pos=(7, 5), name="wb2", white=True)
    else:
        bishop1 = Bishop(board=board, pos=(0, 2), name="bb1", white=False)
        bishop2 = Bishop(board=board, pos=(0, 5), name="bb2", white=False)

    board[bishop1.pos[0]][bishop1.pos[1]] = bishop1
    board[bishop2.pos[0]][bishop2.pos[1]] = bishop2

    return [bishop1, bishop2]
