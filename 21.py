#/usr/bin/env python3

from common import read_input, combine, clean, debug

import re

from dataclasses import dataclass
from collections import Counter
from itertools import islice, product, chain, pairwise


def deterministic(n):
    while True:
        yield from range(1, n+1)


def triple(seq):
    while True:
        yield sum(islice(seq, 3))


def dirac():
    while True:
        yield Dirac([1,2,3])


class Die:
    def __init__(self, source):
        self._source = source

    def __call__(self, n = None):
        if n is None:
            n = 1
        if n < 1:
            raise ValueError("Must roll die at least once, {n} times requested")

        return list(islice(self._source, n))


@dataclass(frozen=True)
class Player:
    space: int
    score: int = 0

    def move(self, n):
        newpos = (self.space + n) % 10
        return Player(newpos, self.score + newpos + 1)


def parse_player(line):
    m = re.match(r"Player ([0-9]+) starting position: ([0-9]+)", line)
    if m:
        return Player(int(m.group(2)) - 1)


def part_one(players):
    np = len(players)

    die = Die(triple(deterministic(100)))

    n = 0
    while players[(n - 1) % np].score < 1000:
        roll ,= die()
        player = players[n % np].move(roll)

        if debug():
            sroll = ""
            match roll:
                case 103:
                    sroll = "100+1+2"
                case 200:
                    sroll = "99+100+1"
                case _:
                    mid = roll//3
                    sroll = f"{mid - 1}+{mid}+{mid + 1}"

            print(f"Player {(n % np) + 1} : {sroll:>9} → {player.space + 1:2d}  score={player.score}")
        players[n % np] = player
        n += 1

    return players[n % np].score * n * 3


def part_two(players):
    turns = [ list() for _ in players ]

    freqs = Counter(map(sum, product([1,2,3], repeat=3)))

    for p, player in enumerate(players):
        turns[p].append(Counter([player]))
        
        while True:
            turn_counter = Counter()
            for pp, nn in turns[p][-1].items():
                if pp.score < 21:
                    for roll, n in freqs.items():
                        newp = pp.move(roll)
                        turn_counter[newp] += n * nn
            turns[p].append(turn_counter)
            if turn_counter.total() == 0:
                break

        # remove the initial player, it was not an actual move
        turns[p].pop(0)


    all_turns = chain.from_iterable(zip(*turns))

    def winloss(ctr, win):
        wls = Counter()
        for p, n in ctr.items():
            wls[p.score >= 21] += n

        return wls[win]

    wins = [ 0 for _ in players ]
    # to make this work for more players, we need something like nwise
    for t, (prev, curr) in enumerate(pairwise(all_turns)):
        p = t % 2
        other_losses = winloss(prev, False)
        my_wins = winloss(curr, True)

        wins[p] += my_wins * other_losses
        

        debug(f"  turn #{t-1:<2}: {wins}")

    return max(wins)


def main():
    players = read_input(combine(parse_player, clean))

    print(f"part  1: {part_one(players[:])}")
    print(f"part  2: {part_two(players[:])}")


if __name__ == "__main__":
    main()
