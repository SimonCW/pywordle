from copy import deepcopy
from dataclasses import dataclass, field
from random import choice
from typing import List, Optional

from structs import Check, Match


def random_strategy(wordlist):
    return choice(wordlist)


def adaptive_strategy_coro(wordlist):
    miss = set()
    yellow = set()
    green = set()
    for word in wordlist:
        cond_no_misses = all([letter not in miss for letter in word])
        cond_match_green = all([word[pos] == l for pos, l in green])
        cond_relocate_yellow = all(
            [(l in word) & (word[pos] != l) for pos, l in yellow]
        )

        if cond_no_misses & cond_match_green & cond_relocate_yellow:
            results = yield word

        # Update sets with results
        for pos, match in enumerate(results):
            if match.check == Check.NotInWord:
                miss.add(match.letter)
            if match.check == Check.Yellow:
                yellow.add((pos, match.letter))
            if match.check == Check.Green:
                green.add((pos, match.letter))


@dataclass
class State:
    n_results_seen: int = 0
    misses: set = field(default_factory=set)
    yellows: set = field(default_factory=set)
    greens: set = field(default_factory=set)

    def update(self, results: Optional[List[Match]]) -> None:
        if results is None:
            return
        self.n_results_seen += 1
        for pos, match in enumerate(results):
            if match.check == Check.NotInWord:
                self.misses.add(match.letter)
            elif match.check == Check.Yellow:
                self.yellows.add((pos, match.letter))
            elif match.check == Check.Green:
                self.greens.add((pos, match.letter))
            else:
                raise ValueError(f"Don't know {match.check}")

    def reset(self) -> None:
        self.n_results_seen = 0
        self.misses.clear()
        self.yellows.clear()
        self.greens.clear()


class AdaptiveStrategy:
    """Avoid words that don't fit the information you have.

    There will be multiple words fitting your current information.
    This strategy doesn't try to find the optimal word to guess from these options
    but will just take the first fitting word from the word list.
    """

    def __init__(self, wordlist: list[str], state: State) -> None:
        self.state = deepcopy(state)
        self.wordlist = wordlist

    def send(self, prev_results) -> str:
        self.state.update(prev_results)
        for word in self.wordlist:
            cond_no_misses = all([letter not in self.state.misses for letter in word])
            cond_match_green = all([word[pos] == l for pos, l in self.state.greens])
            cond_relocate_yellow = all(
                [(l in word) & (word[pos] != l) for pos, l in self.state.yellows]
            )
            if cond_no_misses & cond_match_green & cond_relocate_yellow:
                return word
        print(self.state)
        raise RuntimeError("Ran out of words")


class ChristosStrategy:
    """Always guess the same four words and only then adapt.

    https://www.engineering.columbia.edu/faculty/christos-papadimitriou
    """

    def __init__(self, wordlist: list[str], state: State) -> None:
        self.state = deepcopy(state)
        self.wordlist = wordlist

    def send(self, prev_results) -> str:
        self.state.update(prev_results)
        first_guesses = {0: "handy", 1: "swift", 2: "glove", 3: "crump"}

        if self.state.n_results_seen < 4:
            return first_guesses[self.state.n_results_seen]

        for word in self.wordlist:
            cond_no_misses = all([letter not in self.state.misses for letter in word])
            cond_match_green = all([word[pos] == l for pos, l in self.state.greens])
            cond_relocate_yellow = all(
                [(l in word) & (word[pos] != l) for pos, l in self.state.yellows]
            )
            if cond_no_misses & cond_match_green & cond_relocate_yellow:
                return word
        raise RuntimeError("Ran out of words")
