from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from typing import Callable, Any
from random import randint, shuffle, choice

from graph import DirectedGraph

# TODO: Error checking. Unit tests.


class Game(ABC):  # TODO: implement "state" functionality
    class Player(ABC):
        class Action:
            def __init__(self, player: Game.Player, predicate: Callable[[Game.Player], bool], callback: Callable[[Game.Player, Any], None]) -> None:
                """An action that a player can perform during his turn or out of turn. \n
                Predicate defines if the player can legally perfomr the action. \n
                Callback alters the state of the player and/or the game."""
                self.player: Game.Player = player
                self.predicate = predicate
                self.callback = callback


            def is_legal(self) -> bool:
                return self.predicate(self.player)
            
            
            def do(self, **kwargs) -> None:
                self.callback(self.player, **kwargs)


        def __init__(self, name: str, game: Game) -> None:
            self.name = name
            self.left = None  # player to the left
            self.right = None  # player to the right
            self.game = game
            self.is_playing = False
            self.is_eliminated = False

            # choices is what actions a player can make on his turn or out of turn.
            # choices is a dictionary of name: str and Action class instances.
            # name is returned by the abstract input_handler() method. It can be 
            # from any source: console, GUI input, http request, ...
            self.choices: dict[str, Game.Player.Action] = dict()
            
            # TODO: come up with a better logic for end of turn, end of phase
            # self.add_choice(name="End of turn", predicate=lambda self: self.game.current_phase == "Play", callback=lambda self: (self.is_playing = False))
        

        @abstractmethod
        def choose_move(options: list[str]) -> str:
            return options[0]
        

        def add_choice(self, name: str, predicate: Callable[[Game.Player], bool], callback: Callable[[Game.Player, Any], None]) -> None:
            self.choices[name] = Game.Player.Action(self, predicate, callback)


        def play(self) -> None:
            """Executes actions of a player until his 'end of turn'"""

            # cointinue playing while it's player's turn
            while self.is_playing and not self.is_eliminated and not self.game.is_game_over:
                options = [name for name, action in self.choices.items() if action.is_legal()]
                action = options[0] if len(options) == 1 else self.choose_move(options)

                # TODO: what to do if there are no options?

                self.choices[action].do()
                    

        def __str__(self) -> str:
            return "Game.Player" + self.name
        
    
    class Bot(Player, ABC):
        def __init__(self, name: str, game: Game) -> None:
            super().__init__(name, game)
        
        
        @abstractmethod
        def choose_move(self, options: list[str]) -> str:
            # Implement an algorithm that finds the best move
            best_move = options[0]

            return best_move


    class TurnPhase(Enum):
        DRAW = 1
        PLAY = 2


    def __init__(self):
        self.turn_phases: list[Game.TurnPhase] = [Game.TurnPhase.DRAW, Game.TurnPhase.PLAY]
        self.current_phase: Game.TurnPhase = ""
        self.players: list[Game.Player] = []
        self.min_player_count = 2
        self.max_player_count = 6
        self.clockwise = True
        self._is_game_over = False

    
    def add_player(self, name: str) -> Game.Player:
        player = Game.Player(name=name, game=self)
        self.players.append(player)
        return player


    def add_bot(self, name: str):
        pass

    
    @property
    @abstractmethod
    def is_game_over(self) -> bool:
        """Checks the current state of the game. If the game is over, set self.winners and self.losers"""
        self.is_game_over = True
        return self._is_game_over


    def next_player(self) -> Game.Player:
        return self.current_player.left if self.clockwise else self.current_player.right


    def turn(self) -> None:
        self.current_player.is_playing = True
        for phase in self.turn_phases:
            self.current_phase = phase
            self.current_player.play()
            if self.is_game_over: break
        self.current_player.is_playing = False

    # TODO: create @out_of_turn and @at_the_same_time decorator

    @abstractmethod
    def setup_game(self) -> None:
        # Setting up player order
        shuffle(self.players)
        self.winners: list[Game.Player] = []
        self.losers: list[Game.Player] = []

        # setting left and right players
        self.players.insert(0, self.players[-1])
        self.players.append(self.players[1])
        for i in range(1, len(self.players) - 2):
            self.players[i].left = self.players[i + 1]
            self.players[i].right = self.players[i - 1]
        
        self.players.pop()
        self.players.pop(0)
        self.current_player: Game.Player = self.players[0]


    def start_game(self) -> tuple[list[Game.Player], list[Game.Player]]:
        self.setup_game()

        # returns a tuple of list of winner players and list of lost players
        # TODO: add rounds. One round is when all players have played once
        while not self.is_game_over:
            self.turn(self.current_player)
            self.current_player = self.next_player()
        
        return self.winners, self.losers


class Dice():
    def __init__(self, sides: list = [1, 2, 3, 4, 5, 6]) -> None:
        self.sides = sides

    def roll(self, times: int = 1) -> list:
        rolls = []
        for i in range(times):
            rolls.append(choice(self.sides))

        return rolls

        
class Card(ABC):
    """Abstract class for all card types"""
    def __init__(self, name: str) -> None:
        self.name = name
    

    def __str__(self) -> str:
        return self.name


class Suit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4


CLUBS = Suit.CLUBS
DIAMONDS = Suit.DIAMONDS
HEARTS = Suit.HEARTS
SPADES = Suit.SPADES

SUITS = (CLUBS, DIAMONDS, HEARTS, SPADES)


class FrenchCard(Card):
    """Standard playing cards with one of the following suits: Clubs, Diamonds, Hearts, Spades"""
    def __init__(self, name: str, rank: int, suit: Suit) -> None:
        super().__init__(name)
        self.rank = rank
        self.suit = suit

    
    def __lt__(self, other: FrenchCard) -> bool:
        return self.number < other.number


ACE_OF_CLUBS = FrenchCard(name="A♣️", rank=1, suit=CLUBS)
TWO_OF_CLUBS = FrenchCard(name="2♣️", rank=2, suit=CLUBS)
THREE_OF_CLUBS = FrenchCard(name="3♣️", rank=3, suit=CLUBS)
FOUR_OF_CLUBS = FrenchCard(name="4♣️", rank=4, suit=CLUBS)
FIVE_OF_CLUBS = FrenchCard(name="5♣️", rank=5, suit=CLUBS)
SIX_OF_CLUBS = FrenchCard(name="6♣️", rank=6, suit=CLUBS)
SEVEN_OF_CLUBS = FrenchCard(name="7♣️", rank=7, suit=CLUBS)
EIGHT_OF_CLUBS = FrenchCard(name="8♣️", rank=8, suit=CLUBS)
NINE_OF_CLUBS = FrenchCard(name="9♣️", rank=9, suit=CLUBS)
TEN_OF_CLUBS = FrenchCard(name="10♣️", rank=10, suit=CLUBS)
JACK_OF_CLUBS = FrenchCard(name="J♣️", rank=11, suit=CLUBS)
QUEEN_OF_CLUBS = FrenchCard(name="Q♣️", rank=12, suit=CLUBS)
KING_OF_CLUBS = FrenchCard(name="K♣️", rank=13, suit=CLUBS)

ACE_OF_DIAMONDS = FrenchCard(name="A♦️", rank=1, suit=DIAMONDS)
TWO_OF_DIAMONDS = FrenchCard(name="2♦️", rank=2, suit=DIAMONDS)
THREE_OF_DIAMONDS = FrenchCard(name="3♦️", rank=3, suit=DIAMONDS)
FOUR_OF_DIAMONDS = FrenchCard(name="4♦️", rank=4, suit=DIAMONDS)
FIVE_OF_DIAMONDS = FrenchCard(name="5♦️", rank=5, suit=DIAMONDS)
SIX_OF_DIAMONDS = FrenchCard(name="6♦️", rank=6, suit=DIAMONDS)
SEVEN_OF_DIAMONDS = FrenchCard(name="7♦️", rank=7, suit=DIAMONDS)
EIGHT_OF_DIAMONDS = FrenchCard(name="8♦️", rank=8, suit=DIAMONDS)
NINE_OF_DIAMONDS = FrenchCard(name="9♦️", rank=9, suit=DIAMONDS)
TEN_OF_DIAMONDS = FrenchCard(name="10♦️", rank=10, suit=DIAMONDS)
JACK_OF_DIAMONDS = FrenchCard(name="J♦️", rank=11, suit=DIAMONDS)
QUEEN_OF_DIAMONDS = FrenchCard(name="Q♦️", rank=12, suit=DIAMONDS)
KING_OF_DIAMONDS = FrenchCard(name="K♦️", rank=13, suit=DIAMONDS)

ACE_OF_HEARTS = FrenchCard(name="A❤️", rank=1, suit=HEARTS)
TWO_OF_HEARTS = FrenchCard(name="2❤️", rank=2, suit=HEARTS)
THREE_OF_HEARTS = FrenchCard(name="3❤️", rank=3, suit=HEARTS)
FOUR_OF_HEARTS = FrenchCard(name="4❤️", rank=4, suit=HEARTS)
FIVE_OF_HEARTS = FrenchCard(name="5❤️", rank=5, suit=HEARTS)
SIX_OF_HEARTS = FrenchCard(name="6❤️", rank=6, suit=HEARTS)
SEVEN_OF_HEARTS = FrenchCard(name="7❤️", rank=7, suit=HEARTS)
EIGHT_OF_HEARTS = FrenchCard(name="8❤️", rank=8, suit=HEARTS)
NINE_OF_HEARTS = FrenchCard(name="9❤️", rank=9, suit=HEARTS)
TEN_OF_HEARTS = FrenchCard(name="10❤️", rank=10, suit=HEARTS)
JACK_OF_HEARTS = FrenchCard(name="J❤️", rank=11, suit=HEARTS)
QUEEN_OF_HEARTS = FrenchCard(name="Q❤️", rank=12, suit=HEARTS)
KING_OF_HEARTS = FrenchCard(name="K❤️", rank=13, suit=HEARTS)

ACE_OF_SPADES = FrenchCard(name="A♠️", rank=1, suit=SPADES)
TWO_OF_SPADES = FrenchCard(name="2♠️", rank=2, suit=SPADES)
THREE_OF_SPADES = FrenchCard(name="3♠️", rank=3, suit=SPADES)
FOUR_OF_SPADES = FrenchCard(name="4♠️", rank=4, suit=SPADES)
FIVE_OF_SPADES = FrenchCard(name="5♠️", rank=5, suit=SPADES)
SIX_OF_SPADES = FrenchCard(name="6♠️", rank=6, suit=SPADES)
SEVEN_OF_SPADES = FrenchCard(name="7♠️", rank=7, suit=SPADES)
EIGHT_OF_SPADES = FrenchCard(name="8♠️", rank=8, suit=SPADES)
NINE_OF_SPADES = FrenchCard(name="9♠️", rank=9, suit=SPADES)
TEN_OF_SPADES = FrenchCard(name="10♠️", rank=10, suit=SPADES)
JACK_OF_SPADES = FrenchCard(name="J♠️", rank=11, suit=SPADES)
QUEEN_OF_SPADES = FrenchCard(name="Q♠️", rank=12, suit=SPADES)
KING_OF_SPADES = FrenchCard(name="K♠️", rank=13, suit=SPADES)


CLUBS = (ACE_OF_CLUBS, TWO_OF_CLUBS, THREE_OF_CLUBS, FOUR_OF_CLUBS, FIVE_OF_CLUBS, SIX_OF_CLUBS, SEVEN_OF_CLUBS, EIGHT_OF_CLUBS, NINE_OF_CLUBS, TEN_OF_CLUBS, JACK_OF_CLUBS, QUEEN_OF_CLUBS, KING_OF_CLUBS)
DIAMONDS = (ACE_OF_DIAMONDS, TWO_OF_DIAMONDS, THREE_OF_DIAMONDS, FOUR_OF_DIAMONDS, FIVE_OF_DIAMONDS, SIX_OF_DIAMONDS, SEVEN_OF_DIAMONDS, EIGHT_OF_DIAMONDS, NINE_OF_DIAMONDS, TEN_OF_DIAMONDS, JACK_OF_DIAMONDS, QUEEN_OF_DIAMONDS, KING_OF_DIAMONDS)
HEARTS = (ACE_OF_HEARTS, TWO_OF_HEARTS, THREE_OF_HEARTS, FOUR_OF_HEARTS, FIVE_OF_HEARTS, SIX_OF_HEARTS, SEVEN_OF_HEARTS, EIGHT_OF_HEARTS, NINE_OF_HEARTS, TEN_OF_HEARTS, JACK_OF_HEARTS, QUEEN_OF_HEARTS, KING_OF_HEARTS)
SPADES = (ACE_OF_SPADES, TWO_OF_SPADES, THREE_OF_SPADES, FOUR_OF_SPADES, FIVE_OF_SPADES, SIX_OF_SPADES, SEVEN_OF_SPADES, EIGHT_OF_SPADES, NINE_OF_SPADES, TEN_OF_SPADES, JACK_OF_SPADES, QUEEN_OF_SPADES, KING_OF_SPADES)

ACES = (ACE_OF_CLUBS, ACE_OF_DIAMONDS, ACE_OF_HEARTS, ACE_OF_SPADES)
TWOS = (TWO_OF_CLUBS, TWO_OF_DIAMONDS, TWO_OF_HEARTS, TWO_OF_SPADES)
THREES = (THREE_OF_CLUBS, THREE_OF_DIAMONDS, THREE_OF_HEARTS, THREE_OF_SPADES)
FOURS = (FOUR_OF_CLUBS, FOUR_OF_DIAMONDS, FOUR_OF_HEARTS, FOUR_OF_SPADES)
FIVES = (FIVE_OF_CLUBS, FIVE_OF_DIAMONDS, FIVE_OF_HEARTS, FIVE_OF_SPADES)
SIXES = (SIX_OF_CLUBS, SIX_OF_DIAMONDS, SIX_OF_HEARTS, SIX_OF_SPADES)
SEVENS = (SEVEN_OF_CLUBS, SEVEN_OF_DIAMONDS, SEVEN_OF_HEARTS, SEVEN_OF_SPADES)
EIGHTS = (EIGHT_OF_CLUBS, EIGHT_OF_DIAMONDS, EIGHT_OF_HEARTS, EIGHT_OF_SPADES)
NINES = (NINE_OF_CLUBS, NINE_OF_DIAMONDS, NINE_OF_HEARTS, NINE_OF_SPADES)
TENS = (TEN_OF_CLUBS, TEN_OF_DIAMONDS, TEN_OF_HEARTS, TEN_OF_SPADES)
JACKS = (JACK_OF_CLUBS, JACK_OF_DIAMONDS, JACK_OF_HEARTS, JACK_OF_SPADES)
QUEENS = (QUEEN_OF_CLUBS, QUEEN_OF_DIAMONDS, QUEEN_OF_HEARTS, QUEEN_OF_SPADES)
KINGS = (KING_OF_CLUBS, KING_OF_DIAMONDS, KING_OF_HEARTS, KING_OF_SPADES)


DECK_32 = ACES + SEVENS + EIGHTS + NINES + TENS + JACKS + QUEENS + KINGS

DECK_36 = ACES + SIXES + SEVENS + EIGHTS + NINES + TENS + JACKS + QUEENS + KINGS

DECK_52 = ACES + TWOS + THREES + FOURS + FIVES + SIXES + SEVENS + EIGHTS + NINES + TENS + JACKS + QUEENS + KINGS


class CardGame(Game, ABC):
    class Player(Game.Player, ABC):
        def __init__(self, name: str, game: CardGame) -> None:
            super().__init__(name, game)
            self._hand: list[Card] = []
            self._in_play: list[Card] = []
            
            # TODO: come up with a better logic for end of turn, end of phase
            # self.add_choice(name="End of turn", predicate=lambda self: self.game.current_phase == "Play", callback=lambda self: (self.is_playing = False))
            self.add_choice(name="Discard card", predicate=lambda self: self.hand_size() > 0, callback=CardGame.Player.discard_card)
            self.add_choice(name="Draw", predicate=lambda self: self.game.current_phase == "Draw", callback=CardGame.Player.draw)
            self.add_choice(name="Play a card", predicate=lambda self: self.game.current_phase == "Play" and self.hand_size(), callback=CardGame.Player.play_card)


        @property
        def hand(self) -> list[Card]:
            return self._hand.copy()
        

        @property
        def in_play(self) -> list[Card]:
            return self._in_play.copy()


        def roll_dice(self, count: int = 1) -> int:
            """Roll a 6 sided dice count number of times"""
            roll = 0
            for i in range(count):
                roll += randint(1, 6)
            
            return roll


        def draw_card(self, pile: list[Card]) -> Card:
            """Remove a card from top (tail) of specified pile and append to player's hand"""
            card = pile.pop()
            self.hand.append(card)
            return card
        

        def draw(self, pile: list[Card]) -> None:
            while self.hand_size() < self.game.hand_limit:
                self.draw(pile)


        def hand_size(self) -> int:
            return len(self.hand)
        

        def discard_card(self, pile: list[Card]) -> None:
            card = self.choose_move([card.name for card in self.hand])
            self.hand.remove(card)
            pile.append(card)
        

        def play_card(self, card: Card, callback=lambda: None) -> None:
            self._hand.remove(card)
            self._in_play.append(card)
            callback(card)
                    

        def __str__(self) -> str:
            return "CardGame.Player" + self.name


    class TurnPhase(Enum):
        DRAW = 1
        PLAY = 2


    def __init__(self):
        super().__init__()
        self.turn_phases: list[CardGame.TurnPhase] = [CardGame.TurnPhase.DRAW, CardGame.TurnPhase.PLAY]
        self.current_phase: CardGame.TurnPhase = None
        self.hand_limit: int = 4


class BoardGame(Game, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.dice = Dice()
        self.board: DirectedGraph = None

