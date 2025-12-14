# Ai_Player.py

class AI_Player:
    def __init__(self, color, imp_algorithm):
        self.color = color
        self.imp = imp_algorithm

    def make_move(self, board_obj, opp_color=None, first_move_single=False, moves_played=0):
        if opp_color is None:
            opp_color = 1 if self.color == 2 else 2

        best_move, score = self.imp.choose_move(board_obj, self.color, opp_color)
        if not best_move:
            return None, None

        # Handle first move exception (only one stone allowed)
        if first_move_single and moves_played == 0 and len(best_move) > 1:
            best_move = [best_move[0]]

        # Apply the move combo at once
        board_obj.apply_move(best_move, self.color)
        return best_move, score