# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands

```bash
# Set Python path (required before running)
export PYTHONPATH=.

# Run the game
python3 Chess/ChessGame.py
```

**Dependencies:** PyGame and NumPy
```bash
python3 -m pip install -U pygame numpy --user
```

There is no formal test framework. A `test()` function exists in `ChessGame.py:481` that runs random moves for stress testing.

## Architecture Overview

This is a Python chess engine with Pygame GUI supporting human vs AI gameplay.

### Layer Structure

1. **UI Layer** (`ChessGame.py`) - Pygame event loop, board rendering, user input handling
2. **Game Logic Layer** (`ChessEngine.py`) - Board state management via `chessBoard` class
3. **AI Layer** (`Computation.py`) - Minimax with alpha-beta pruning, piece-square evaluation tables
4. **Piece Models** (`ChessPieces/`) - Each piece type has its own module with move generation

### Key Classes

- `chessBoard` (`ChessEngine.py:15`) - Central game state: 8x8 NumPy board array, piece dictionaries (`whitePieces`/`blackPieces`), castling rights (`Castle` dict), move history (`moveLog` deque)
- `Computation` (`Computation.py:7`) - AI with configurable depth (levels 0-4), position evaluation using material + piece-square tables
- `Move` (`Move.py`) - Move representation with special move detection (castling, en passant, promotion)
- `Piece` base class (`ChessPieces/Piece.py`) - All pieces inherit from this, each implements `getValidMoves()`

### Game Flow

1. `settings()` displays difficulty menu (keys 0-4 or 'e' for notation editor)
2. Creates `chessBoard` instance with standard starting position
3. `main()` loop: player moves via mouse clicks, AI responds via `Computation.moveCompute()`
4. Moves validated by generating all legal moves, applying each, checking if king is in check, then undoing

### Special Rules Implementation

- **Castling**: Tracked in `Castle` dict (piece→boolean), validated in `King.isLegalCastle()`
- **En passant**: Detected by examining `moveLog` for opponent's last pawn double-move
- **Promotion**: Pawn auto-promotes to queen via `Pawn.promote()`/`unPromote()`

### Notation System

Moves use simple 4-character notation: `e2e4` (start square + end square). Static mappings in `Move` class convert between chess notation and array indices.

### Controls

- **Mouse click**: Select and move pieces
- **Z key**: Undo last move
- **0-4 keys**: Select AI difficulty at start screen
- **E key**: Open notation editor to replay games
