from Chess.Move import Move
from Chess.ChessPieces.Piece import Piece
import numpy as np


class Knight(Piece):
    def __init__(self, board: np.ndarray, pos: tuple, name: str, white: bool) -> None:
        super(Knight, self).__init__(board=board, pos=pos, name=name, white=white)

    def getValidMoves(self) -> list:
        """
            computing all legal moves for a knight piece in the board
            :return: validMoves after insertions
        """
        validMoves = []
        row, col = self.pos[0], self.pos[1]  # saving position
        # all ahead steps for a knight
        knightMoves = {1: (1, 2), 2: (2, 1), 3: (1, -2), 4: (2, -1), 5: (-1, -2), 6: (-2, -1), 7: (-1, 2), 8: (-2, 1)}
        for i in range(1, 9):  # iterate for every step in dictionary
            r, c = knightMoves[i]  # saving steps
            if 0 <= row + r <= 7 and 0 <= col + c <= 7:  # if ahead position is inside board
                curPiece = self.board[row + r][col + c]  # picking piece in that position
                if curPiece is None:
                    newMove = Move(startLoc=(row, col), endLoc=(row + r, col + c), board=self.board)
                    validMoves.append(newMove)
                    continue
                # checking for a possible next position for a knight
                if self.white and not curPiece.white:
                    newMove = Move(startLoc=(row, col), endLoc=(row + r, col + c), board=self.board)
                    validMoves.append(newMove)
                elif not self.white and curPiece.white:
                    newMove = Move(startLoc=(row, col), endLoc=(row + r, col + c), board=self.board)
                    validMoves.append(newMove)
        return validMoves


def main(board: np.ndarray, white: bool) -> list:
    if white:
        knight1 = Knight(board=board, pos=(7, 1), name="wk1", white=True)
        knight2 = Knight(board=board, pos=(7, 6), name="wk2", white=True)
    else:
        knight1 = Knight(board=board, pos=(0, 1), name="bk1", white=False)
        knight2 = Knight(board=board, pos=(0, 6), name="bk2", white=False)

    board[knight1.pos[0]][knight1.pos[1]] = knight1
    board[knight2.pos[0]][knight2.pos[1]] = knight2

    return [knight1, knight2]
