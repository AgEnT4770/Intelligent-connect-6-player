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

    def make_move(self, board_obj, use_alpha_beta=False, opp_color=None):
        """
        board_obj: Board object
        use_alpha_beta: لو True هنستخدم imp.alphabeta (نفترض imp هو AlphaBeta)
        opp_color: لون الخصم (لو None نفترض 3 - self.color)
        يرجع tuple من الخانات اللي اتحطت فيها الحجارة
        """
        if opp_color is None:
            opp_color = 1 if self.color == 2 else 2

        valid_moves = self.get_valid_moves(board_obj.grid)
        if not valid_moves:
            return None

        # استخدام AlphaBeta لو imp من النوع AlphaBeta وطلبت ذلك
        if use_alpha_beta and isinstance(self.imp, AlphaBeta):
            best_move, score = self.imp.choose_move(board_obj.grid, self.color, opp_color)
        else:
            # Minimax
            best_move, score = self.imp.choose_move(board_obj.grid, self.color, opp_color)

        if best_move is None:
            return None

        # تطبيق الحركة على Board object نفسه
        board_obj.apply_move(best_move, self.color)

        return best_move

