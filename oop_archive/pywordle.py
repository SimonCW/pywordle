from copy import deepcopy
from pathlib import Path
from random import choice, seed
from statistics import mean
from typing import Generator

from tqdm import tqdm

from strategies import (AdaptiveStrategy, ChristosStrategy, State,
                        adaptive_strategy_coro, random_strategy)
from structs import Check, Match


def main():
    wordlist = read_wordle_words("words_wordle.txt")

    init_game_stats = {"n_games": len(wordlist), "n_wins": 0, "n_guesses": []}
    strat_stats = {}
    strategies = [
        AdaptiveStrategy(wordlist, state=State()),
        ChristosStrategy(wordlist, state=State()),
    ]
    for strategy in strategies:
        game_stats = deepcopy(init_game_stats)
        for _ in tqdm(range(game_stats["n_games"]), desc="Playing Games"):
            target = choice(wordlist)
            #  print(target, "-" * 5, sep="\n")
            strategy.state.reset()
            results = None
            for i in range(1, 7):
                guess = strategy.send(results)
                results = list(compare(guess, target))
                #      print("".join([str(match) for match in results]))
                if all(m.check == Check.Green for m in results):
                    game_stats["n_wins"] += 1
                    game_stats["n_guesses"].append(i)
                    break
        strat_stats[type(strategy).__name__] = game_stats

    for strat, game_stats in strat_stats.items():
        print(
            20 * "-",
            "\n",
            f"{strat = }, \n"
            f"Games won = {game_stats['n_wins'] / game_stats['n_games'] * 100}%, \n"
            f"avg winning guess = {mean(game_stats['n_guesses'])} \n",
            f"n_games = {game_stats['n_games'] = }, \n",
        )


def read_wordle_words(words_file="words"):
    # Wordlist is copied from `/usr/share/dict/words` on MacOs
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


if __name__ == "__main__":
    main()
