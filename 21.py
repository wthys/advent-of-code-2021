#/usr/bin/env python3

from common import read_input, combine, clean, debug, color, sign

import re

from itertools import islice
from dataclasses  import dataclass


def deterministic(n):
    while True:
        yield from [ i + 1 for i in range(n) ]


@dataclass(frozen=True)
class DieRoll:
    rolls: list[int]

    def __str__(self):
        return '+'.join(map(str, self.rolls))

    def __int__(self):
        return sum(self.rolls)


class Die:
    def __init__(self, source):
        self._source = source

    def __mul__(self, n):
        if int(n) != n:
            raise ValueError(f"Cannot multiply Die with {type(n)}")

        s = sign(n, int)
        if s == 0:
            raise ValueError(f"Must multiply Die with 0")

        n = abs(n)
        return DieRoll(list(map(lambda v: s * v, islice(self._source, n))))


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
    players = players[:]
    print(players)

    np = len(players)

    die = Die(deterministic(100))

    def pn(n):
        return (n % np) + 1

    n = 0
    while players[(n - 1) % np].score < 1000:
        roll = die * 3
        player = players[n % np].move(int(roll))
        debug(f"{str(roll):>9} Player {pn(n)} → {player.space + 1:2d} 🏆={player.score}")
        players[n % np] = player
        n += 1

    return players[n % np].score * n * 3


def part_two(players):
    return 'n/a'


def main():
    players = read_input(combine(parse_player, clean))

    print(f"part  1: {part_one(players)}")
    print(f"part  2: {part_two(players)}")


if __name__ == "__main__":
    main()
