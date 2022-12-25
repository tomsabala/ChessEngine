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

    def endGame(self, kingPos: tuple) -> end:
        """
        functions will be called only when player has no moves available
        and will check if king is on threat
        :return: boolean value true iff check-mate
        """
        king = self.engine.board[kingPos[0]][kingPos[1]]
        if king.isCheck():
            if king.white and self.engine.whiteTurn:
                return self.end.WHITE
            if not king.white and not self.engine.whiteTurn:
                return self.end.BLACK
        return self.end.DRAW
