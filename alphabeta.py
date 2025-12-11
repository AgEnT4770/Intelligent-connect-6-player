class AlphaBeta :
    def __init__(self,max_depth,heuristic_func):
        self.max_depth = max_depth
        self.heuristic_func = heuristic_func

    def get_moves(self, board):
        N = len (board)
        moves = []
        for r in range(N):
            for c in range(N):
                if board[r][c] == 0 :
                    move.append((r,c))
        return moves

def alphabeta(self, board, alpha, beta, is_maximizing, my_player, opp_player):
    if debth == self.max_depth:
        return self.heuristic_func(board, my_player, opp_player)
    
    moves = self.get_moves(board)

    if not moves:
        return self.heuristic_func(board, my_player, opp_player)

    if is_maximizing:
        best_score = float('-inf')
        for (r,c) in moves:
            board[r][c] = my_player
            score = self.alphabeta(board, debth + 1, alpha, beta,False, my_player, opp_player)
            board[r][c] = 0
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break
        return best_score

    else :
        best_score = float('inf')
        for (r,c) in moves :
            board[r][c] =opp_player
            score = alphabeta(board, debth +1, alpha, beta, True, my_player,opp_player)
            board[r][c] = 0
            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if beta <= alpha:
                break
        return best_score

