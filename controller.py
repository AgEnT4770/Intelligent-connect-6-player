# controller.py

class HumanPlayer:
    def __init__(self, color):
        self.color = color

class GameController:
    def __init__(self, board, player1, player2, first_move_single=True):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.game_over = False
        self.winner = None
        self.first_move_single = first_move_single
        self._moves_played = 0

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def play_move(self, move_combo):
        if self.game_over:
            return None
        if self.first_move_single and self._moves_played == 0:
            if isinstance(move_combo, tuple) and isinstance(move_combo[0], int):
                move_combo = [move_combo]
            elif isinstance(move_combo, list) and len(move_combo) > 1:
                move_combo = [move_combo[0]]

        player_color = self.current_player.color
        try:
            self.board.apply_move(move_combo, player_color)
        except ValueError:
            return None

        self._moves_played += 1
        if self.board.check_win(player_color):
            self.game_over = True
            self.winner = self.current_player
        elif self.board.check_draw():
            self.game_over = True
            self.winner = None
        else:
            self.switch_player()
        return move_combo

    def ai_move(self):
        if self.game_over or not hasattr(self.current_player, "make_move"):
            return None, None
        move, score = self.current_player.make_move(
            self.board,
            opp_color=(1 if self.current_player.color == 2 else 2),
            first_move_single=self.first_move_single,
            moves_played=self._moves_played
        )
        if move:
            self._moves_played += 1
            if self.board.check_win(self.current_player.color):
                self.game_over = True
                self.winner = self.current_player
            elif self.board.check_draw():
                self.game_over = True
                self.winner = None
            else:
                self.switch_player()
        return move, score