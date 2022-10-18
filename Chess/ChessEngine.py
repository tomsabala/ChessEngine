"""
this class responsible for
generate moves
board evaluation
minimax
and alpha beta pruning
"""
from collections import deque
from enum import Enum
from Chess.ChessPieces import King, Queen, Bishop, Knight, Rook, Pawn
from Chess.Move import Move


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


class chessBoard:
    def __init__(self, *args):
        """
        presenting board as 8X8 np array,
        blank spot - "--",
        white piece - "w_", black piece - "b_",
        Rook, Knight, Bishop etc. - "_r", "_k", "_b" and so on.
        """
        if len(args) > 0:
            self.board = args[0]
            self.blackPieces = args[1]
            self.whitePieces = args[2]
            self.kingPos = args[3]
            self.Castle = args[4]
            self.dictCastleLog = args[5]
            self.whiteTurn = args[6]
            self.moveLog = args[7]
        else:
            self.board = [[None, None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None, None]]
            # black and white pieces' dictionary for positions etc. uses to eval game state
            self.blackPieces = {}
            self.whitePieces = {}

            self.Castle = {}
            self.kingPos = {}

            self.buildKing()
            self.buildQueen()
            self.buildBishops()
            self.buildKnights()
            self.buildRooks()
            self.buildPawn()

            self.dictCastleLog = {}
            # game turn-log
            self.whiteTurn = True  # a boolean obj. for whose turn is it
            self.moveLog = deque()  # an array of all moves

    def __copy__(self):
        return chessBoard(self.board, self.blackPieces, self.whitePieces, self.kingPos, self.Castle, self.dictCastleLog,
                          self.whiteTurn, self.moveLog)

    def makeMove(self, move: Move) -> None:
        """
        initial move as a play on the board
        """
        piece = move.selectedPiece
        if isinstance(piece, King.King):
            self.kingPos[piece.white] = (move.rowEnd, move.colEnd)

        # updating board
        self.updateBoard(move=move)

        # updating piece and castle dictionary
        move.selectedPiece.makeMove(move=move)
        self.updatePieces(move=move, white=self.whiteTurn)
        self.moveLog.append(move)  # appending the move to memory
        self.whiteTurn = not self.whiteTurn  # switching turns

    def updateBoard(self, move: Move) -> None:
        """
        updating board according to move annotation, after a move is done
        :param move: Move type object
        :return: None
        """
        if move.castling:  # for a castling move
            # updating king position on board
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece
            self.board[move.rowStart][move.colStart] = None
            # updating rook position on board
            if move.colEnd < move.colStart:  # for a left side castling
                self.board[move.rowEnd][move.colEnd + 1] = move.capturedPiece
                self.board[move.rowStart][0] = None
            else:  # for a right side castling
                self.board[move.rowEnd][move.colEnd - 1] = move.capturedPiece
                self.board[move.rowStart][7] = None
            move.capturedPiece.makeMove(move=move, isCastle=True)

        elif move.enPassant:  # for an en-passant move
            # updating selected and captured positions on board
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece
            self.board[move.rowStart][move.colStart] = None
            self.board[move.rowStart][move.colEnd] = None
        elif move.promotion:  # for a promotion move
            # updating piece presenting + updating board position
            move.selectedPiece.promote()
            self.board[move.rowStart][move.colStart] = None
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece
        else:  # for a regular move
            # updating selected piece position
            self.board[move.rowStart][move.colStart] = None
            self.board[move.rowEnd][move.colEnd] = move.selectedPiece

    def updatePieces(self, move: Move, white: bool) -> None:
        """
        updating pieces dictionaries according to move annotation, after a move is made
        :param move: Move type object
        :param white: boolean type, True iff move is a white piece move
        :return: None
        """
        # boolean to piece color dictionary
        dictTurnUpdates = {True: self.whitePieces, False: self.blackPieces}
        if move.castling:  # for a castling move
            # updating king piece
            dictTurnUpdates[white][move.selectedPiece] = move.rowEnd, move.colEnd
            # updating rook piece
            if move.colEnd < move.colStart:  # left side castling
                dictTurnUpdates[white][move.capturedPiece] = move.rowEnd, move.colEnd + 1
            else:  # right side castling
                dictTurnUpdates[white][move.capturedPiece] = move.rowEnd, move.colEnd - 1
            # updating castling state dictionary
            self.dictCastleLog[move.moveID] = self.Castle.copy()
            self.Castle[move.capturedPiece] = False
            self.Castle[move.selectedPiece] = False
        elif move.enPassant:  # for an an-passant move
            # updating selected piece
            dictTurnUpdates[white][move.selectedPiece] = move.rowEnd, move.colEnd
            # deleting captured piece
            del dictTurnUpdates[not white][move.capturedPiece]
        elif move.promotion:  # for a promotion move
            # adding new presenting
            dictTurnUpdates[white][move.selectedPiece] = move.rowEnd, move.colEnd
        else:  # for a regular move
            # updating selected piece
            dictTurnUpdates[white][move.selectedPiece] = move.rowEnd, move.colEnd
            # updating captured piece of needed
            if move.capturedPiece in dictTurnUpdates[not white].keys():
                del dictTurnUpdates[not white][move.capturedPiece]
            # update captured piece castle state if needed
            if move.capturedPiece in self.Castle and self.Castle[move.capturedPiece]:
                self.dictCastleLog[move.moveID] = self.Castle.copy()
                self.Castle[move.capturedPiece] = False
            # update selected piece castle state if needed
            if move.selectedPiece in self.Castle and self.Castle[move.selectedPiece]:
                self.dictCastleLog[move.moveID] = self.Castle.copy()
                self.Castle[move.selectedPiece] = False

    def undoMove(self, move: Move) -> None:
        """
        resetting board to last move
        """
        # restoring board
        self.restoreBoard(move=move)
        # restoring pieces of needed
        move.selectedPiece.undoMove(move=move)
        self.restorePieces(move=move, white=self.whiteTurn)
        try:
            if not self.whiteTurn and self.board[move.rowStart][move.colStart].name == "wX":
                self.kingPos[True] = (move.rowStart, move.colStart)
            if self.whiteTurn and self.board[move.rowStart][move.colStart].name == "bX":
                self.kingPos[False] = (move.rowStart, move.colStart)
        except AttributeError:
            pass
        # updating settings
        self.whiteTurn = not self.whiteTurn
        self.moveLog.pop()

    def restoreBoard(self, move: Move) -> None:
        """
        restoring board state according to move annotation, after a move is undo
        :param move: a Move type object
        :return: None
        """
        if move.castling:  # for a castling move
            # updating king position on board
            self.board[move.rowStart][move.colStart] = move.selectedPiece
            self.board[move.rowEnd][move.colEnd] = None
            # updating rook position on board
            if move.colEnd < move.colStart:  # left side castling
                self.board[move.rowStart][0] = move.capturedPiece
                self.board[move.rowEnd][move.colEnd + 1] = None
            else:  # eight side castling
                self.board[move.rowStart][7] = move.capturedPiece
                self.board[move.rowEnd][move.colEnd - 1] = None

            move.capturedPiece.undoMove(move=move, isCastle=True)
        elif move.enPassant:  # for an en-passant move
            # updating selected and captured positions on board
            self.board[move.rowEnd][move.colEnd] = None
            self.board[move.rowStart][move.colEnd] = move.capturedPiece
            self.board[move.rowStart][move.colStart] = move.selectedPiece
        elif move.promotion:  # for a promotion move
            # updating piece on board
            move.selectedPiece.unPromote()
            self.board[move.rowStart][move.colStart] = move.selectedPiece
            self.board[move.rowEnd][move.colEnd] = None
        else:  # for a regular move
            # updating board
            self.board[move.rowEnd][move.colEnd] = move.capturedPiece
            self.board[move.rowStart][move.colStart] = move.selectedPiece

    def restorePieces(self, move: Move, white: bool) -> None:
        """
        restoring pieces dictionaries according to move annotation, after a move is undo
        :param move: Move type object
        :param white: boolean type obj. True iff it's a white piece move
        :return: None
        """
        # boolean to color dictionary
        dictTurnUpdates = {True: self.whitePieces, False: self.blackPieces}
        if move.castling:  # for a castling move
            # updating king in dictionary
            dictTurnUpdates[not white][move.selectedPiece] = move.rowStart, move.colStart
            # updating rook in dictionary
            if move.colEnd < move.colStart:  # left side castling
                dictTurnUpdates[not white][move.capturedPiece] = move.rowStart, 0
            else:  # right side castling
                dictTurnUpdates[not white][move.capturedPiece] = move.rowStart, 7
            # updating castle state
            self.Castle = self.dictCastleLog[move.moveID]
            del self.dictCastleLog[move.moveID]
        elif move.enPassant:  # for an en-passant move
            # updating selected piece and captured piece
            dictTurnUpdates[not white][move.selectedPiece] = move.rowStart, move.colStart
            dictTurnUpdates[white][move.capturedPiece] = move.rowEnd, move.colStart
        elif move.promotion:  # for a promotion move
            # updating new presenting of selected piece
            dictTurnUpdates[not white][move.selectedPiece] = move.rowStart, move.colStart
        else:  # for a regular move
            # updating selected piece
            dictTurnUpdates[not white][move.selectedPiece] = move.rowStart, move.colStart
            # updating captured piece if needed
            if move.capturedPiece is not None:
                dictTurnUpdates[white][move.capturedPiece] = move.rowEnd, move.colEnd
            # updating castling state if needed
            if move.moveID in self.dictCastleLog:
                self.Castle = self.dictCastleLog[move.moveID]
                del self.dictCastleLog[move.moveID]

    # noinspection PyUnresolvedReferences
    def getValidMoves(self) -> list:
        """
        computing all valid games on board
        :return: an array of all possible valid move on board
        """
        validMoves = []  # an empty array
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece is None:
                    continue
                # noinspection PyUnresolvedReferences
                if piece.white and self.whiteTurn:
                    if isinstance(piece, King.King):
                        validMoves += piece.getValidMoves(castleDict=self.Castle)
                    elif isinstance(piece, Pawn.Pawn):
                        validMoves += piece.getValidMoves(moveLog=self.moveLog)
                    else:
                        # noinspection PyUnresolvedReferences
                        validMoves += piece.getValidMoves()
                if not piece.white and not self.whiteTurn:
                    if isinstance(piece, King.King):
                        validMoves += piece.getValidMoves(castleDict=self.Castle)
                    elif isinstance(piece, Pawn.Pawn):
                        validMoves += piece.getValidMoves(moveLog=self.moveLog)
                    else:
                        validMoves += piece.getValidMoves()

        result = []
        # validation check
        for move in validMoves:
            self.makeMove(move=move)  # apply move
            r, c = self.kingPos[not self.whiteTurn]
            king = self.board[r][c]
            if not king.isCheck():  # check for validation
                result.append(move)
            self.undoMove(move=move)  # undo move

        return result

    def buildRooks(self) -> None:
        rooks = Rook.main(board=self.board, white=False)
        for rook in rooks:
            self.blackPieces[rook] = rook.pos
            self.Castle[rook] = True

        rooks = Rook.main(board=self.board, white=True)
        for rook in rooks:
            self.whitePieces[rook] = rook.pos
            self.Castle[rook] = True

    def buildBishops(self) -> None:
        bishops = Bishop.main(board=self.board, white=False)
        for bishop in bishops:
            self.blackPieces[bishop] = bishop.pos

        bishops = Bishop.main(board=self.board, white=True)
        for bishop in bishops:
            self.whitePieces[bishop] = bishop.pos

    def buildKnights(self) -> None:
        knights = Knight.main(board=self.board, white=False)
        for knight in knights:
            self.blackPieces[knight] = knight.pos

        knights = Knight.main(board=self.board, white=True)
        for knight in knights:
            self.whitePieces[knight] = knight.pos

    def buildPawn(self) -> None:
        pawns = Pawn.main(board=self.board, white=False)
        for pawn in pawns:
            self.blackPieces[pawn] = pawn.pos

        pawns = Pawn.main(board=self.board, white=True)
        for pawn in pawns:
            self.whitePieces[pawn] = pawn.pos

    def buildKing(self) -> None:
        bKing = King.main(board=self.board, white=False)
        self.blackPieces[bKing] = bKing.pos
        self.kingPos[False] = bKing.pos
        self.Castle[bKing] = True

        wKing = King.main(board=self.board, white=True)
        self.whitePieces[wKing] = wKing.pos
        self.kingPos[True] = wKing.pos
        self.Castle[wKing] = True

    def buildQueen(self) -> None:
        bQueen = Queen.main(board=self.board, white=False)
        self.blackPieces[bQueen] = bQueen.pos

        wQueen = Queen.main(board=self.board, white=True)
        self.whitePieces[wQueen] = wQueen.pos
