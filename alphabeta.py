# alphabeta.py

import copy
from itertools import combinations
from heuristics import heuristic1, heuristic2
from minimax import check_win

class AlphaBeta:
    def __init__(self, max_depth, heuristic_func, stones_per_move=2, win_k=6):
        self.max_depth = max_depth
        self.heuristic_func = heuristic_func
        self.stones_per_move = stones_per_move
        self.win_k = win_k

    def get_moves(self, board):
        N = len(board)
        moves = []
        for r in range(N):
            for c in range(N):
                if board[r][c] == 0:
                    moves.append((r,c))
        return moves

    def evaluate_terminal(self, board, my_player, opp_player, depth):
        if check_win(board, my_player, self.win_k):
            return float('inf')
        if check_win(board, opp_player, self.win_k):
            return float('-inf')
        moves = self.get_moves(board)
        if depth >= self.max_depth or not moves:
            return self.heuristic_func(board, my_player, opp_player)
        return None

    def alphabeta(self, board, depth, alpha, beta, is_maximizing, my_player, opp_player):
        term = self.evaluate_terminal(board, my_player, opp_player, depth)
        if term is not None:
            return None, term

        moves = self.get_moves(board)
        move_combinations = list(combinations(moves, min(self.stones_per_move, len(moves))))

        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for combo in move_combinations:
                for (r,c) in combo:
                    board[r][c] = my_player
                _, score = self.alphabeta(board, depth + 1, alpha, beta, False, my_player, opp_player)
                for (r,c) in combo:
                    board[r][c] = 0
                if score is not None and score > best_score:
                    best_score = score
                    best_move = combo
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_move, best_score
        else:
            best_score = float('inf')
            best_move = None
            for combo in move_combinations:
                for (r,c) in combo:
                    board[r][c] = opp_player
                _, score = self.alphabeta(board, depth + 1, alpha, beta, True, my_player, opp_player)
                for (r,c) in combo:
                    board[r][c] = 0
                if score is not None and score < best_score:
                    best_score = score
                    best_move = combo
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_move, best_score

    def choose_move(self, board, my_player, opp_player):
        move, score = self.alphabeta(board, 0, float('-inf'), float('inf'), True, my_player, opp_player)
        return move, score
