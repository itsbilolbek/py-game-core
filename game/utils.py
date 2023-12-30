from collections.abc import Sequence
from typing import Callable


class CursesInput:
    # TODO: implement checkbox and radio for curses
    pass


class StandardInput:
    """Standard input and output methods for console applications"""
    def out(stream: str, end: str="\n") -> None:
        print(str, end=end)

    # TODO: reimplement generalized checkbox and radio with error handling

    def checkbox(options: Sequence[str], required = True) -> set[str]:
        chosen = set()
        next_input = StandardInput.radio(options, required)

        while next_input:            
            chosen.add(next_input)
            next_input = StandardInput.radio(options, False)
        
        return chosen
        
    
    def radio(options: Sequence[str], required = True) -> str:        
        chosen = StandardInput.in_string()
        if chosen == "" and not required: return None

        while chosen not in options:
            StandardInput.out("Invalid option")
            
            chosen = StandardInput.in_string()
            if chosen == "" and not required: return None
        
        return chosen


    def in_string() -> str:
        return input()


    def in_integer() -> int:
        pass


    def in_decimal() -> int:
        pass

