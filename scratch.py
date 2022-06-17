from copy import deepcopy
from dataclasses import dataclass, field


@dataclass
class State:
    n_results_seen: int = 0
    misses: set = field(default_factory=set)
    yellows: set = field(default_factory=set)
    greens: set = field(default_factory=set)


@dataclass(frozen=True)
class State:
    n_results_seen: int = 0
    misses: set = field(default_factory=set)
    yellows: set = field(default_factory=set)
    greens: set = field(default_factory=set)


s = State()
s.misses.add("a")
s.n_results_seen += 1
print(s)
