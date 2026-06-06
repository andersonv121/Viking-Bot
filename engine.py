import chess
import random
from chess.engine import PlayResult
from lib.engine_wrapper import MinimalEngine

depth = 3
print ("depth is ", depth)

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
}

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]

piece_tables = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE,
}

def evaluate(board):
        
    score = 0

    for piece_type in piece_values:
        score += len(board.pieces(piece_type, board.turn)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, not board.turn)) * piece_values[piece_type]

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        
        if piece.color == chess.WHITE:
            bonus = piece_tables[piece.piece_type][square]
        else:
            bonus = piece_tables[piece.piece_type][chess.square_mirror(square)]

        if piece.color == board.turn:
            score += bonus
        else:
            score -= bonus

    return score

##def minimax(board, depth):
  ##  if depth == 0 or board.is_game_over():
    ##    return evaluate(board)
##
  ##  best_score = -99999
    ##for move in board.legal_moves:
      ##  board.push(move)
        ##score = -minimax(board, depth - 1)
        ##score = -alphabeta(board, depth - 1, -beta, -alpha)
  ##      board.pop()
  ##      best_score = max(best_score, score)
  ## 
  ##  return best_score
  ## 

def alpha_beta(board, depth, alpha, beta):
    if board.is_checkmate():
       return -100000 - depth

    if depth == 0 or board.is_game_over():
        return evaluate(board)
    
    for move in board.legal_moves:
        board.push(move)
        score = -alpha_beta(board, depth-1, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

def get_best_move(board):
    best_moves = []
    best_score = -99999

    for move in board.legal_moves:
        board.push(move)

        ##if board.is_checkmate():
          ##  board.pop()
          ##  return move
    
        score = -alpha_beta(board, depth - 1, -99999, 99999)        
        ##score = -minimax(board, depth-1)
        board.pop()

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)
