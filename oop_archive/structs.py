from dataclasses import dataclass
from enum import Enum


class Check(Enum):
    Green = 42
    Yellow = 43
    NotInWord = 40


@dataclass
class Match:
    letter: str
    check: Check

    def __str__(self):
        # Ansi escape code hack by Cameron
        return f"\033[97;{self.check.value};1m{self.letter}\033[0m"
