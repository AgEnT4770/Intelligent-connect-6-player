# Ai_Player.py

class AI_Player:
    def __init__(self, color, imp_algorithm):
        """
        AI player wrapper.
        :param color: 1 or 2 (player color)
        :param imp_algorithm: search engine instance (Minimax or AlphaBeta)
        """
        self.color = color
        self.imp = imp_algorithm

    def make_move(self, board_obj, opp_color=None, first_move_single=False, moves_played=0):
        """
        Choose and apply a move using the search algorithm.
        Enforces Connect-6 rule: first move = one stone, subsequent moves = two stones.
        :param board_obj: Board instance
        :param opp_color: Opponent color (1 or 2)
        :param first_move_single: Boolean, whether first move is restricted to one stone
        :param moves_played: Number of moves already played in the game
        :return: (best_move, score)
        """
        if opp_color is None:
            opp_color = 1 if self.color == 2 else 2

        # Ask the search algorithm for the best move
        best_move, score = self.imp.choose_move(board_obj, self.color, opp_color)

        if not best_move:
            return None, None

        # First move exception: force single stone
        if first_move_single and moves_played == 0:
            if isinstance(best_move, list) and len(best_move) > 1:
                best_move = [best_move[0]]
            elif isinstance(best_move, tuple):
                best_move = [best_move]

        # Normalize to list of tuples before applying
        if isinstance(best_move, tuple):
            best_move = [best_move]

        board_obj.apply_move(best_move, self.color)
        return best_move, score
