from game import Game


class RockPaperScissors(Game):
    class Player(Game.Player):
        def choose_move(options: list[str]) -> str:
            return super().choose_move()


    def setup_game(self):
        return super().setup_game()
    

    @property
    def is_game_over(self) -> bool:
        pass
