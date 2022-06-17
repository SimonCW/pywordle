from random import choice

from structs import State


class RandomStrategy:
    def __init__(self, wordlist: list[str]) -> None:
        self.wordlist = wordlist

    def __call__(self, state=None):
        return choice(self.wordlist)


class AdaptiveStrategy:
    """Avoid words that don't fit the information you have.

    There will be multiple words fitting your current information.
    This strategy doesn't try to find the optimal word to guess from these options
    but will just take the first fitting word from the word list.
    """

    def __init__(self, wordlist: list[str]) -> None:
        self.wordlist = wordlist

    def __call__(self, state: State) -> str:
        for word in self.wordlist:
            cond_no_misses = all([letter not in state.misses for letter in word])
            cond_match_green = all([word[pos] == l for pos, l in state.greens])
            cond_relocate_yellow = all(
                [(l in word) & (word[pos] != l) for pos, l in state.yellows]
            )
            if cond_no_misses & cond_match_green & cond_relocate_yellow:
                return word
        raise RuntimeError(f"Ran out of words, current state: {state}")


class ChristosStrategy:
    """Always guess the same four words and only then adapt guesses to state.

    Interestingly this has a 100% win rate but needs more guesses than the
    `AdaptiveStrategy`

    https://www.engineering.columbia.edu/faculty/christos-papadimitriou
    """

    def __init__(self, wordlist: list[str]) -> None:
        self.wordlist = wordlist

    def __call__(self, state) -> str:
        first_guesses = {0: "handy", 1: "swift", 2: "glove", 3: "crump"}

        if state.n_results_seen < 4:
            return first_guesses[state.n_results_seen]

        for word in self.wordlist:
            cond_no_misses = all([letter not in state.misses for letter in word])
            cond_match_green = all([word[pos] == l for pos, l in state.greens])
            cond_relocate_yellow = all(
                [(l in word) & (word[pos] != l) for pos, l in state.yellows]
            )
            if cond_no_misses & cond_match_green & cond_relocate_yellow:
                return word
        raise RuntimeError(f"Ran out of words, current state: {state}")


def adaptive_strategy_coro(wordlist, state=State()):
    for word in wordlist:
        cond_no_misses = all([letter not in state.misses for letter in word])
        cond_match_green = all([word[pos] == l for pos, l in state.greens])
        cond_relocate_yellow = all(
            [(l in word) & (word[pos] != l) for pos, l in state.yellows]
        )

        if cond_no_misses & cond_match_green & cond_relocate_yellow:
            state = yield word
