# ai_player.py

from minimax import Minimax
from alphabeta import AlphaBeta

class AI_Player:
    def __init__(self, color, imp_algorithm):
        """
        color: 1 أو 2
        imp_algorithm: كائن من Minimax أو AlphaBeta
        """
        self.color = color
        self.imp = imp_algorithm  # افتراض: imp لديه choose_move(board, my_player, opp_player)

    def get_valid_moves(self, board):
        N = len(board)
        moves = []
        for r in range(N):
            for c in range(N):
                if board[r][c] == 0:
                    moves.append((r,c))
        return moves

    def make_move(self, board, use_alpha_beta=False, opp_color=None):
        """
        board: list[list[int]]
        use_alpha_beta: لو True هنستخدم imp.alphabeta (نفترض imp هو AlphaBeta)
        opp_color: لون الخصم (لو None نفترض 3 - self.color)
        يرجع tuple من الخانات اللي اتحطت فيها الحجارة
        """
        if opp_color is None:
            opp_color = 1 if self.color == 2 else 2

        valid_moves = self.get_valid_moves(board)
        if not valid_moves:
            return None

        # استخدام AlphaBeta لو imp من النوع AlphaBeta وطلبت ذلك
        if use_alpha_beta and isinstance(self.imp, AlphaBeta):
            best_move, score = self.imp.choose_move(board, self.color, opp_color)
        else:
            # Minimax
            best_move, score = self.imp.choose_move(board, self.color, opp_color)

        if best_move is None:
            return None

        # best_move قد تكون tuple من مواقع (combo)
        for (r,c) in best_move:
            board[r][c] = self.color

        return best_move
