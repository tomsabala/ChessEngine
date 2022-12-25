from Chess.Move import Move
from Chess.ChessPieces.Bishop import Bishop
from Chess.ChessPieces.Rook import Rook
from Chess.ChessPieces.Piece import Piece
import numpy as np


class Pawn(Piece):
    def __init__(self, board: np.ndarray, pos: tuple, name: str, white: bool) -> None:
        super(Pawn, self).__init__(board=board, pos=pos, name=name, white=white)
        self.isPromoted = False
        self.rook_bishop = None

    def getValidMoves(self, moveLog=None) -> list:
        """
            func. computes all valid moves of the piece
            :param moveLog: array of all last moves
            :return: validMoves after insertion of all valid moves for piece pawn
        """
        validMoves = []
        row, col = self.pos  # saving pawn position
        if self.isPromoted:
            return self.rook_bishop[0].getValidMoves() + self.rook_bishop[1].getValidMoves()
        if self.white:  # white's position
            if row - 1 >= 0:  # if it can move forward
                if self.board[row - 1][col] is None:  # position one ahead is empty
                    newMove = Move(startLoc=(row, col), endLoc=(row - 1, col), board=self.board)  # create move
                    validMoves.append(newMove)  # insert move
                    # pawn at initial position and two ahead is empty
                    if row == 6 and self.board[row - 2][col] is None:
                        newMove = Move(startLoc=(row, col), endLoc=(row - 2, col), board=self.board)
                        validMoves.append(newMove)
                if 0 <= col - 1:
                    piece = self.board[row - 1][col - 1]
                    if isinstance(piece, Piece) and piece.isBlack():  # diagonal from left is with a black piece
                        newMove = Move((row, col), (row - 1, col - 1), self.board)
                        validMoves.append(newMove)
                if col + 1 <= 7:
                    piece = self.board[row - 1][col + 1]
                    if isinstance(piece, Piece) and piece.isBlack():  # diagonal from right is with a black piece
                        newMove = Move(startLoc=(row, col), endLoc=(row - 1, col + 1), board=self.board)
                        validMoves.append(newMove)
                if row == 3:
                    # all 6 next lines refer to en Passant move
                    lastMove = moveLog[-1]
                    opt1 = 1 * (col + 1) + 10 * row + 100 * (col + 1) + 1000 * (row - 2)
                    opt2 = 1 * (col - 1) + 10 * row + 100 * (col - 1) + 1000 * (row - 2)
                    if lastMove.selectedPiece.isBlackPawn() and lastMove.moveID == opt1 and col + 1 <= 7:
                        newMove = Move(startLoc=(row, col), endLoc=(row - 1, col + 1), board=self.board, enPassant=True)
                        validMoves.append(newMove)
                    if lastMove.selectedPiece.isBlackPawn() and lastMove.moveID == opt2 and col - 1 >= 0:
                        newMove = Move(startLoc=(row, col), endLoc=(row - 1, col - 1), board=self.board, enPassant=True)
                        validMoves.append(newMove)

        else:  # it is a black move turn
            if row + 1 <= 7:  # can move forward
                if self.board[row + 1][col] is None:  # on ahead is empty
                    newMove = Move(startLoc=(row, col), endLoc=(row + 1, col), board=self.board)  # create move
                    validMoves.append(newMove)  # insert move
                    if row == 1 and self.board[row + 2][col] is None:  # pawn os on initial position two ahead is empty
                        newMove = Move(startLoc=(row, col), endLoc=(row + 2, col), board=self.board)
                        validMoves.append(newMove)
                if 0 <= col - 1:
                    piece = self.board[row + 1][col - 1]
                    if isinstance(piece, Piece) and piece.isWhite():  # diagonal from right is with a white piece
                        newMove = Move(startLoc=(row, col), endLoc=(row + 1, col - 1), board=self.board)
                        validMoves.append(newMove)
                if col + 1 <= 7:
                    piece = self.board[row + 1][col + 1]
                    if isinstance(piece, Piece) and piece.isWhite():  # diagonal from left is with a white piece
                        newMove = Move(startLoc=(row, col), endLoc=(row + 1, col + 1), board=self.board)
                        validMoves.append(newMove)
                if row == 4:
                    # all 6 next line refer to en Passant move
                    lastMove = moveLog[-1]
                    opt1 = 1 * (col + 1) + 10 * row + 100 * (col + 1) + 1000 * (row + 2)
                    opt2 = 1 * (col - 1) + 10 * row + 100 * (col - 1) + 1000 * (row + 2)
                    if lastMove.selectedPiece.isWhitePawn() and lastMove.moveID == opt1 and col + 1 <= 7:
                        newMove = Move(startLoc=(row, col), endLoc=(row + 1, col + 1), board=self.board, enPassant=True)
                        validMoves.append(newMove)
                    if lastMove.selectedPiece.isWhitePawn() and lastMove.moveID == opt2 and col - 1 >= 0:
                        newMove = Move(startLoc=(row, col), endLoc=(row + 1, col - 1), board=self.board, enPassant=True)
                        validMoves.append(newMove)
        return validMoves

    def promote(self) -> None:
        self.isPromoted = True
        self.rook_bishop = (Bishop(board=self.board, pos=self.pos, name=self.name, white=self.white),
                            Rook(board=self.board, pos=self.pos, name=self.name, white=self.white))
        self.name = self.name[0] + "qp" + self.name[-1]

    def unPromote(self) -> None:
        self.isPromoted = False
        self.rook_bishop = None
        self.name = self.name[0] + "p" + self.name[-1]

    def makeMove(self, move: Move) -> None:
        super().makeMove(move=move)
        if self.isPromoted:
            self.rook_bishop[0].makeMove(move=move)
            self.rook_bishop[1].makeMove(move=move)

    def undoMove(self, move: Move) -> None:
        super().undoMove(move=move)
        if self.isPromoted:
            self.rook_bishop[0].undoMove(move=move)
            self.rook_bishop[1].undoMove(move=move)


def main(board: np.ndarray, white: bool) -> list:
    color2prop = {True: ("w", 6), False: ("b", 1)}
    pawns = []

    for i in range(8):
        pawn = Pawn(board=board,
                    pos=(color2prop[white][1], i),
                    name=color2prop[white][0]+"p"+str(i),
                    white=white)
        pawns.append(pawn)
        board[pawn.pos[0]][pawn.pos[1]] = pawn

    return pawns
