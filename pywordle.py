from pathlib import Path
from random import choice
from statistics import mean
from typing import Optional

from strategies import (AdaptiveStrategy, ChristosStrategy, RandomStrategy,
                        adaptive_strategy_coro)
from structs import Check, Match, State

try:
    from tqdm import tqdm
except ImportError:

    def tqdm(iterator, *args, **kwargs):
        return iterator


def main():
    wordlist = read_wordle_words("words_wordle.txt")

    n_games = len(wordlist)
    strat_stats = {}
    strategies = [
        RandomStrategy(wordlist),
        AdaptiveStrategy(wordlist),
        ChristosStrategy(wordlist),
    ]
    for strategy in strategies:
        game_stats = {"n_games": n_games, "n_wins": 0, "n_guesses": []}
        for _ in tqdm(range(n_games), desc="Playing Games"):
            target = choice(wordlist)
            #  print(target, "-" * 5, sep="\n")
            results = None
            state = State()
            for i in range(1, 7):
                guess = strategy(state)
                results = list(compare(guess, target))
                state = update_state(state, results=results)
                #      print("".join([str(match) for match in results]))
                if all(m.check == Check.Green for m in results):
                    game_stats["n_wins"] += 1
                    game_stats["n_guesses"].append(i)
                    break
        strat_stats[type(strategy).__name__] = game_stats
    print_results(strat_stats)


def read_wordle_words(words_file="words"):
    basedir = Path().absolute()
    wordsfile = basedir / words_file

    def is_wordle_conform(word):
        return all([len(word) == 5, word.islower(), word.isascii(), word.isalpha()])

    with wordsfile.open() as f:
        wordlist = [word.strip() for word in f if is_wordle_conform(word.strip())]
    return wordlist


def compare(guess, target):
    for gl, tl in zip(guess, target):
        if gl == tl:
            yield Match(gl, Check.Green)
        elif gl in target:
            yield Match(gl, Check.Yellow)
        else:
            yield Match(gl, Check.NotInWord)


def update_state(state: State, results: Optional[list[Match]]) -> State:
    if results:
        state.n_results_seen += 1
        for pos, match in enumerate(results):
            if match.check == Check.NotInWord:
                state.misses.add(match.letter)
            elif match.check == Check.Yellow:
                state.yellows.add((pos, match.letter))
            elif match.check == Check.Green:
                state.greens.add((pos, match.letter))
    return state


def print_results(strat_stats: dict) -> None:
    for strat, game_stats in strat_stats.items():
        print(
            20 * "-",
            "\n",
            f"{strat = }, \n"
            f"Games won = {game_stats['n_wins'] / game_stats['n_games'] * 100}%, \n"
            f"avg winning guess = {mean(game_stats['n_guesses'])} \n",
            f"n_games = {game_stats['n_games']}, \n",
        )


if __name__ == "__main__":
    main()
