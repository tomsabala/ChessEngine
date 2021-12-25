import numpy as np


class Computation:
    """
    this class responsible for th computational part of the engine
    it used minimax algorithm and alpha-beta pruning

    in addition, it's declaring the strategy of the engine
    """
    # this dictionary is a piece score dictionary
    piecesScore = {"K": 200, "q": 9, "r": 5,
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
                         "wk": whiteKnightControl, "wq": whiteQueenControl, "wK": whiteKingControl,
                         "bp": blackPawnControl, "br": blackRookControl, "bb": blackBishopControl,
                         "bk": blackKnightControl, "bq": blackQueenControl, "bK": blackKingControl}

    def __init__(self, level):
        """
        computational unit
        :param level: minimax depth
        """
        self.lvl = level

    def moveCompute(self, engine, validMoves):
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
        return self.minimax(self.lvl, engine, validMoves, maximize=True)[1]

    def minimax(self, depth, engine, validMoves, maximize, alpha=float("-inf"), beta=float("inf")):
        """
        algorithm return a minimized/maximized score and the move who lead to it
        :param depth: minimax tree depth
        :param engine: game state, include board, piece and so on
        :param validMoves: all valid moves at current
        :param maximize: boolean type, true iff we want to maximize move gain
        :param alpha: min bar to fall in a loss,
        if we found a loss smaller than alpha there is no need to continue in its sub-trees
        :param beta: a top bar to fall in a gain,
        if we found a gain bigger than beta there is no need to continue in its sub-trees
        :return: a tuple of score and a move
        """
        if depth == 0 or len(validMoves) == 0:  # base case, depth is zero
            return self.evalPosition(engine), engine.moveLog[-1]  # return evaluation of engine state and the last move
        bestMove = None  # initial a best-move indicator
        if maximize:  # if we want to maximize player gain
            Eval = float("-inf")  # evaluation score
            for move in validMoves:  # we want to every move evaluate position afterwards
                engine.makeMove(move, True)  # play move
                # evaluate vest move score
                currEval = self.minimax(depth-1, engine, engine.getValidMoves(), False, alpha, beta)[0]
                # checkin whether eval is bigger than currEval
                if currEval > Eval:
                    Eval = currEval
                    bestMove = move
                # return move backwards
                engine.undoMove(True)
                # updating alpha
                alpha = max(alpha, currEval)
                # pruning tree
                if beta <= alpha:
                    break
        else:
            # this block is pretty much similar to the one above, only now we want to minimize player loss
            Eval = float("inf")
            for move in validMoves:
                engine.makeMove(move, True)
                currEval = self.minimax(depth-1, engine, engine.getValidMoves(), True, alpha, beta)[0]
                if currEval < Eval:
                    Eval = currEval
                    bestMove = move
                engine.undoMove(True)
                beta = min(beta, currEval)
                if alpha >= beta:
                    break
        return Eval, bestMove

    def evalPosition(self, engine):
        """
        evaluating position
        :param engine: game state, includes turn, board and so on...
        :return: return position score
        """
        # strategy... (need to be improved)
        return self.materialPieces(engine) + self.boardControl(engine)

    def materialPieces(self, engine):
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
                if piece[0] == "w":  # if piece belongs to the whites
                    whiteScore += self.piecesScore[piece[1]]
                elif piece[0] == "b":  # if piece belongs to the blacks
                    blackScore += self.piecesScore[piece[1]]
        return blackScore - whiteScore  # score

    def boardControl(self, engine):
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
                if piece[0] == "w":  # piece belongs to the whites
                    whiteScore += self.piecesControl[piece[:2]][r][c]
                elif piece[0] == "b":  # piece belongs to the blacks
                    blackScore += self.piecesControl[piece[:2]][r][c]
        return blackScore - whiteScore  # score
