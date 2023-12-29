from __future__ import annotations
from collections.abc import Sequence
from abc import abstractmethod
from typing import Callable, Any

class Program:
    # TODO: implement "state" functionality and event handlers
    # TODO: Add input streams (wasd, menu, mouse, ...)
    # TODO: input streams
    class User:
        class Action:
            def __init__(self, player: Program.User, predicate: Callable[[Program.User], bool], callback: Callable[[Program.User, Any], None]) -> None:
                """An action that a player can perform during his turn or out of turn. \n
                Predicate defines if the player can legally perfomr the action. \n
                Callback alters the state of the player and/or the game."""
                self.player = player
                self.predicate = predicate
                self.callback = callback


            @property
            @abstractmethod
            def is_legal(self) -> bool:
                return self.predicate(self.player)
            
            
            async def run(self, **kwargs) -> None:
                self.callback(self.player, **kwargs)


        def __init__(self, name: str, game: Program) -> None:
            self.name = name
            self.game = game
            self.is_eliminated = False
            self.checkbox = None
            self.radio = None

            # choices is what actions a player can make on his turn or out of turn.
            # choices is a dictionary of name: str and Action class instances.
            # name is returned by the abstract input_handler() method. It can be 
            # from any source: console, GUI input, http request, ...
            self.choices: dict[str, Program.User.Action] = dict()
            
            # TODO: come up with a better logic for end of turn, end of phase
            # self.add_choice(name="End of turn", predicate=lambda self: self.game.current_phase == "Play", callback=lambda self: (self.is_playing = False))


        # TODO: define getters and setters

        @abstractmethod
        async def choose_action(self, options: Sequence) -> str:
            return self.radio(options)


        def add_choice(self, name: str, predicate: Callable[[Program.User], bool], callback: Callable[[Program.User, Any], None]) -> None:
            self.choices[name] = Program.User.Action(self, predicate, callback)


        async def use(self) -> None:
            """Executes actions of a player until his 'end of turn'"""
            # TODO: action menu vs move menu. A player may have lost, but still should have access to menu
            # cointinue playing while it's player's turn

            options = [name for name, action in self.choices.items() if action.is_legal]
            action = options[0] if len(options) == 1 else await self.choose_action(options)

            # TODO: what to do if there are no options?

            await self.choices[action].run()

        
        def leave_program(self) -> None:
            # TODO: on leave event
            self.game.users.remove(self)
            pass
                    

        def __str__(self) -> str:
            return "Application.Player" + self.name
            

    def __init__(self):
        self.users: set[Program.User] = set(Program.User("admin"))
        self.application_process = Graph()

        self.current_state = self.application_process.add_node(Program.setup)
        

        self.process = [
            {Program.State.START: self._start_program},
            {
                Program.State.SETUP: self.setup,
                Program.State.LOOP: self._loop_wrapper
            },
            {}
        ]

        self.current_state = None

    
    @property
    def users_count(self) -> int:
        return len(self.users)

    
    def add_user(self, name: str) -> User:
        player = Program.User(name=name, game=self)
        self.users.add(player)
        return player
    

    def discard_user(self, player: User) -> User:
        if isinstance(player, Program.User):
            self.users.discard(player)


    def add_bot(self, name: str) -> Bot:
        bot = Bot(name, self)
        self.users.add(bot)
        return bot
    

    def discard_bot(self, bot: Bot) -> Bot:
        self.discard_user(bot)


    @abstractmethod
    def setup(self) -> None:
        # Setting up player order
        shuffle(self.users)
        self.winners: list[Program.User] = []
        self.losers: list[Program.User] = []

        return Program.State.LOOP


    @abstractmethod
    def loop(self) -> None:
        pass
    

    async def _loop_wrapper(self):
        while not self.is_game_over:
            for player in self.users:
                player.use()
            return self.loop()


    def _start_program(self):
        """Run setup_game, run game loop asyncronously and return a tuple of winners and losers"""
        self.setup()

        asyncio.run(self._loop_wrapper())

        return Program.State.SETUP
