from typing import Any, Callable
from game import *
from random import shuffle

from game import Player


class DurakPlayer(Player):
    def next_action(self) -> Callable[[Player], Any]:
        action = input()
        match (action):
            case "end turn":
                return DurakPlayer.end_turn()
            case _:
                print("Invalid command. Try again")
                return self.next_action()

class DurakGame(CardGame):
    class Player(CardGame.Player):
        def next_action(self) -> Callable[[Player], Any]:
            action = input()
            match (action):
                case "end turn":
                    return DurakPlayer.end_turn()
                case _:
                    print("Invalid command. Try again")
                    return self.next_action()
                
            
    def __init__(self, players: list[Player]):
        super().__init__(players)
        
        self.draw_pile = list(DECK_36)
        shuffle(self.draw_pile)
        
        self.trump_card = self.draw_pile[0]
        self.current_player = player[0]

        lowest = 14  # imaginary out of bound maximum card to determine lowest trump card

        for i in range(6):
            for player in self.players:
                card = player.draw_card(self.draw_pile)
                
                if card.suit == self.trump_card and card.number < lowest:
                    self.current_player = player
                    lowest = card.number
    

    def turn(self, player: Player):
        if player.hand_size() == 0:
            return

        # take cards until there are 6 cards in hand
        for i in range(len(self.players)):
            if len(self.draw_pile) > 0:
                while player.hand_size() < 6:
                    player.draw_card(self.draw_pile)
            
            player = player.left
    

    def get_trump(self) -> Suit:
        return self.trump_card.suit


    def is_game_over(self) -> bool:
        count = 0
        for player in self.players:
            if player.hand_size() > 0:
                count += 1

        return count <= 1