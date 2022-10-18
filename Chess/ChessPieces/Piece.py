import Chess.Move


class Piece:
    def __init__(self, board: list, pos: tuple, name: str, white: bool) -> None:
        self.board = board
        self.pos = pos
        self.name = name
        self.white = white
        self.id = (pos, name)

    def makeMove(self, move: Chess.Move.Move) -> None:
        self.pos = move.rowEnd, move.colEnd

    def undoMove(self, move: Chess.Move.Move) -> None:
        self.pos = move.rowStart, move.colStart

    def isBlackPawn(self) -> bool:
        return isinstance(self, Chess.ChessPieces.Pawn.Pawn) and not self.white

    def isWhitePawn(self) -> bool:
        return isinstance(self, Chess.ChessPieces.Pawn.Pawn) and self.white

    def isWhiteKing(self) -> bool:
        return isinstance(self, Chess.ChessPieces.King.King) and self.white

    def isBlackKing(self) -> bool:
        return isinstance(self, Chess.ChessPieces.King.King) and not self.white

    def isWhite(self) -> bool:
        return self.white

    def isBlack(self) -> bool:
        return not self.white

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Piece):
            return False
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.id)
