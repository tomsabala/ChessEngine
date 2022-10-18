import ChessEngine
import numpy as np
from Chess.ChessEngine import chessBoard
from Chess.Move import Move


class Computation:
    """
    this class responsible for th computational part of the engine
    it used minimax algorithm and alpha-beta pruning

    in addition, it's declaring the strategy of the engine
    """
    # this dictionary is a piece score dictionary
    piecesScore = {"X": 200, "q": 9, "r": 5,
                   "b": 3, "k": 3, "p": 1}
    # all next matrices are a board control units seperated by piece type and color
    # white king board control
    whiteKingControl = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                        [-2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]
    # white queen board control
    whiteQueenControl = [[-2.0, -2.0, -1.0, -0.5, -0.5, -1.0, -2.0, -2.0],
                         [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                         [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                         [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                         [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0],
                         [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -1.0],
                         [-1.0, 0.0, 0.5, 0.0, 0.0, 0.5, 0.0, -1.0],
                         [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]
    # white rook board control
    whiteRookControl = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]
    # white bishop board control
    whiteBishopControl = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                          [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                          [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                          [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                          [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                          [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                          [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                          [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]
    # white knight board control
    whiteKnightControl = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                          [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                          [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                          [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                          [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                          [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                          [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                          [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]
    # white pawn board control
    whitePawnControl = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    # black king board control
    blackKingControl = whiteKingControl[::-1]
    # black queen board control
    blackQueenControl = whiteQueenControl[::-1]
    # black rook board control
    blackRookControl = whiteRookControl[::-1]
    # black bishop board control
    blackBishopControl = whiteBishopControl[::-1]
    # black knight board control
    blackKnightControl = whiteKnightControl[::-1]
    # black pawn board control
    blackPawnControl = whitePawnControl[::-1]
    # a dictionary of piece type to board control matrix
    piecesControl = {"wp": whitePawnControl, "wr": whiteRookControl, "wb": whiteBishopControl,
                     "wk": whiteKnightControl, "wq": whiteQueenControl, "wX": whiteKingControl,
                     "bp": blackPawnControl, "br": blackRookControl, "bb": blackBishopControl,
                     "bk": blackKnightControl, "bq": blackQueenControl, "bX": blackKingControl}

    def __init__(self, level: int) -> None:
        """
        computational unit
        :param level: minimax depth
        """
        self.lvl = level

    def moveCompute(self, engine: chessBoard, validMoves: list) -> Move:
        """
        here we start the process of computing a smart move
        :param engine: engine parameter state, includes board, turn, pieces and so on.
        :param validMoves: array of all valid moves
        :return: a selected move
        """
        if self.lvl == 0:  # if level is zero engine selects a random move
            move = np.random.choice(validMoves)
            return move
        # return a move from minimax algo.
        return self.minimax(depth=self.lvl, engine=ChessEngine.chessBoard.__copy__(engine),
                            validMoves=validMoves, maximize=True)[1]

    def minimax(self, depth: int, engine: chessBoard, validMoves: list, maximize: bool, alpha=float("-inf"),
                beta=float("inf")) -> tuple:
        """
        algorithm return a minimized/maximized score and the move who lead to it
        :param depth: minimax tree depth
        :param engine: game state, include board, piece and so on
        :param validMoves: all valid moves at current
        :param maximize: boolean type, true iff we want to maximize move gain
        :param alpha: min bar to fall in a loss,
        if we found a loss smaller than alpha there is no need to continue in its subtrees
        :param beta: a top bar to fall in a gain,
        if we found a gain bigger than beta there is no need to continue in its subtrees
        :return: a tuple of score and a move
        """
        if depth == 0 or len(validMoves) == 0:  # base case, depth is zero
            #  return evaluation of engine state and the last move
            return self.evalPosition(engine=engine), engine.moveLog[-1]
        bestMove = None  # initial a best-move indicator
        if maximize:  # if we want to maximize player gain
            eval = float("-inf")  # evaluation score
            for move in validMoves:  # we want to every move evaluate position afterwards
                engine.makeMove(move=move)  # play move
                # evaluate vest move score
                currEval = self.minimax(depth=depth - 1, engine=engine, validMoves=engine.getValidMoves(),
                                        maximize=False, alpha=alpha, beta=beta)
                # return move backwards
                engine.undoMove(move=move)
                # checkin whether eval is bigger than currEval
                if currEval[0] > eval:
                    eval = currEval[0]
                    bestMove = move
                # updating alpha
                alpha = max(alpha, currEval[0])
                # pruning tree
                if beta <= alpha:
                    return eval, bestMove
        else:
            # this block is pretty much similar to the one above, only now we want to minimize player loss
            eval = float("inf")
            for move in validMoves:
                engine.makeMove(move=move)
                currEval = self.minimax(depth=depth - 1, engine=engine, validMoves=engine.getValidMoves(),
                                        maximize=True, alpha=alpha, beta=beta)
                engine.undoMove(move=move)
                if currEval[0] < eval:
                    eval = currEval[0]
                    bestMove = move
                beta = min(beta, currEval[0])
                if alpha >= beta:
                    return eval, bestMove
        return eval, bestMove

    def evalPosition(self, engine: chessBoard) -> float:
        """
        evaluating position
        :param engine: game state, includes turn, board and so on...
        :return: return position score
        """

        def penalty(e: chessBoard) -> int:
            r, c = e.kingPos[False]
            king = e.board[r][c]
            if king.isCheck():
                return -5
            return 0

        def bonus(e):
            r, c = e.kingPos[True]
            king = e.board[r][c]
            if king.isCheck():
                return 5
            return 0

        # strategy... (need to be improved)
        materialScore = self.materialPieces(engine=engine)
        boardScore = self.boardControl(engine=engine)
        bonus = bonus(e=engine)
        penalty = penalty(e=engine)
        return materialScore + boardScore + bonus + penalty

    def materialPieces(self, engine: chessBoard) -> float:
        """
        evaluating pieces materials
        :param engine: game state
        :return: return black material score (black piece - white piece)
        """
        # initial score chanel
        whiteScore = 0
        blackScore = 0
        # for every position compute piece score and add to the relevant chanel
        for r in range(8):
            for c in range(8):
                piece = engine.board[r][c]  # current piece
                if piece is None:
                    continue
                if piece.white:  # if piece belongs to the whites
                    whiteScore += self.piecesScore[piece.name[1]]
                else:  # if piece belongs to the blacks
                    blackScore += self.piecesScore[piece.name[1]]
        return blackScore - whiteScore  # score

    def boardControl(self, engine: chessBoard) -> float:
        """
        evaluating board control
        :param engine: game state
        :return: return black board control score
        """
        # initial score chanel
        whiteScore = 0
        blackScore = 0
        # for every piece, compute piece board control and add to the relevant chanel
        for r in range(8):
            for c in range(8):
                piece = engine.board[r][c]  # curr piece
                if piece is None:
                    continue
                if piece.white:  # piece belongs to the whites
                    whiteScore += self.piecesControl[piece.name[:2]][r][c]
                else:  # piece belongs to the blacks
                    blackScore += self.piecesControl[piece.name[:2]][r][c]
        return blackScore - whiteScore  # score
