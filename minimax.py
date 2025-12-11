class Minimax :
    def __init__(self,max_depth , heuristic_func):
        self.max_depth = max_depth
        self.heuristic_func = heuristic_func

    def get_moves(self,board):
        N = len(board)
        moves = []
        for r in range(N):
            for c in range(N):
                if board[r][c] == 0:
                    move.append((r,c))
        return moves

    def Minimax(self,board,depth,is_maximizing,my_player,opp_player):
        
        if depth == self.max_depth:
            return self.heuristic_func(board,my_player,opp_player)

        moves = self.get_moves(board)
        if not moves :
            return self.heuristic_func(board,my_player,opp_player)
    
        if is_maximizing:
            best_score = float('-inf')
            for (r,c) in moves:
                board[r][c] = my_player
                score = self.Minimax(board,debth + 1,False,my_player,opp_player)
                board[r][c] = 0
                best_score = max(best_score, score)
            return best_score

        else :
            best_score = float('inf')
            for (r , c) in moves :
                board[r][c] = opp_player
                score = self.Minimax(board,debth + 1,True, my_player,opp_player)
                board[r][c] = 0
                best_score = min(best_score, score)
            return best_score
