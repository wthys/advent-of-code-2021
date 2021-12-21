#/usr/bin/env python3

from common import read_input, combine, clean, debug, color

import multiprocessing as mp
import operator
import os
import re

from dataclasses import dataclass
from collections import Counter
from functools import reduce, cache
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
        debug(f"Player {(n % np) + 1} : {roll:>3} → {player.space + 1:2d} 🏆={player.score}")
        players[n % np] = player
        n += 1

    return players[n % np].score * n * 3


@dataclass(frozen=True)
class Result:
    winner: int
    state: list[int]
    rolls: list[int]

    def done(self):
        return self.winner is not None


@cache
def move_player(space, roll):
    newpos = (space + roll) % 10
    return newpos

def play_game(players, die, threshold):
    np = len(players)
    players = [p.space for p in players]
    scores = [0 for _ in players]

    rolls = []

    while True:
        for p, roll in enumerate(die(np)):
            if roll is None:
                return Result(None, None, None)
            rolls.append(roll)
            players[p] = move_player(players[p], roll)
            scores[p] += 1 + players[p]
            if scores[p] >= threshold:
                return Result(p, scores, rolls)


def winners(players, turns):
    np = len(players)
    nr = turns
    freqs = Counter(map(sum, product([1,2,3], repeat=3)))
    wins = [0 for _ in range(np)]

    def collect(result):
        if result.done():
            inter = map(lambda r: freqs[r], result.rolls)
            wins[result.winner] += reduce(operator.mul, inter, 1)

    for x in [1]:
    #with mp.Pool(mp.cpu_count()) as pool:

        for reality in product(freqs, repeat=turns):
            def deter():
                yield from reality
                yield None

            #pool.apply_async(play_game, (players, Die(deter()), 21), callback=collect)
            collect(play_game(players, Die(deter()), 21))
            if debug():
                print(f"  {color.FAINT}{turns:>3}:{color.END} {' - '.join(map(str, wins))}", end = '\r')

    #    pool.close()
    #    pool.join()

    return wins


def winners2(players):
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

        turns[p].pop(0)

    wins = [ 0 for _ in players ]

    all_turns = chain.from_iterable(zip(*turns))
    losses = 1

    def wl(ctr):
        wls = Counter()
        for p, n in ctr.items():
            wls[p.score >= 21] += n

        return wls[False], wls[True]

    for t, (prev, ctr) in enumerate(pairwise(all_turns)):
        #if t < len(players):
        #    continue
        #prev = all_turns[t - 1]
        p = t % len(players)
        other = wl(prev)
        my = wl(ctr)
        debug(f" Player {(p+1) % 2 + 1}: wins {other[1]} - {other[0]} losses")

        losses *= other[0]

        wins[p] += my[1] * other[0]
        

        debug(f"  turn #{t-1:<2}: {wins}")

    return max(wins)






            




class Split:
    def __init__(self, players, turn):
        self.players = list(players)
        self.turn = turn
        self.children = dict()
        self.done = sum(map(lambda s: s.score >= 21, players)) > 0

    def resolve(self):
        if self.done:
            return 0

        active = self.turn % len(self.players)
        for roll in Counter( sum(dice) for dice in product([1,2,3], repeat=3) ):
           players = self.players[:]
           players[active] = players[active].move(roll)
           self.children[roll] = Split(players, self.turn + 1)


        return len(self.children)

    def wins(self, multiplier):
        wins = list(map(lambda p: p.score >= 21), self.players)
        if self.done:
            return wins

        for roll, split in self.children.items():
            mult = multiplier(roll)
            for idx, w in enumerate(split.wins()):
                wins[idx] += mult * w

        return wins

    def depth(self):
        if self.done:
            return 0

        if len(self.children) == 0:
            return 0

        return 1 + max( child.depth() for child in self.children.values() )

    def __iter__(self):
        yield from self.children.values()

    def __str__(self):
        return f"Split(p={self.players}, t={self.turn}, d={[0,1][self.done]})"


def part_two(players):

    return winners2(players)

    return 'n/a'

    old_wins = None
    wins = [0 for _ in players]
    turn = 1

    while (sum(wins) == 0 or old_wins != wins) and turn <= 1000:
        old_wins = wins[:]

        wins = winners(players[:], turn)
        if debug():
            print(f"  {color.FAINT}{turn:>6}: {wins}", end = "\r")
        turn += 1
    

    return max(wins)


def main():
    players = read_input(combine(parse_player, clean))

    print(f"part  1: {part_one(players[:])}")
    print(f"part  2: {part_two(players[:])}")


if __name__ == "__main__":
    main()
