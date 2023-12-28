from game import TurnBasedGame


class RockPaperScissors(TurnBasedGame):
    class Player(TurnBasedGame.Player):
        def choose_action(options: list[str]) -> str:
            return super().choose_action()


    def setup_game(self):
        return super().setup_game()
    

    @property
    def is_game_over(self) -> bool:
        pass
