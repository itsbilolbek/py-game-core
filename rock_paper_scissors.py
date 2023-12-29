from game.game import TurnBasedGame


class RockPaperScissors(TurnBasedGame):
    class Player(TurnBasedGame.Player):
        def choose_action(options: list[str]) -> str:
            return super().choose_action()


    def setup(self):
        return super().setup()
    

    @property
    def is_game_over(self) -> bool:
        pass
