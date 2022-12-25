from Chess.ChessPieces.Bishop import Bishop
from Chess.ChessPieces.Rook import Rook
from Chess.ChessPieces.Piece import Piece
from Chess.Move import Move
import numpy as np


class Queen(Piece):
    def __init__(self, board: np.ndarray, pos: tuple, name: str, white: bool) -> None:
        super(Queen, self).__init__(board=board, pos=pos, name=name, white=white)
        self.bishopQ = Bishop(board=board, pos=pos, name=name, white=white)
        self.rookQ = Rook(board=board, pos=pos, name=name, white=white)

    def getValidMoves(self) -> list:
        """
        computing all legal moves for a queen piece in the board
        :return: validMoves after insertions
        """
        return self.bishopQ.getValidMoves() + self.rookQ.getValidMoves()

    def makeMove(self, move: Move) -> None:
        super().makeMove(move=move)
        self.rookQ.makeMove(move=move)
        self.bishopQ.makeMove(move=move)

    def undoMove(self, move: Move) -> None:
        super().undoMove(move=move)
        self.rookQ.undoMove(move=move)
        self.bishopQ.undoMove(move=move)


def main(board: np.ndarray, white: bool) -> Queen:
    color2prop = {True: ("w", 7), False: ("b", 0)}
    queen = Queen(board=board,
                  pos=(color2prop[white][1], 4),
                  name=color2prop[white][0]+"q",
                  white=white)

    board[queen.pos[0]][queen.pos[1]] = queen

    return queen
