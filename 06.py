#!/usr/bin/env python3

import re

from itertools import chain
from collections import Counter

from common import read_input, debug


class School:
    def __init__(self, fishes):
        self.generations = Counter(fishes)

    def age(self):
        newgen = Counter()
        for gen, amount in self.generations.items():
            if gen == 0:
                newgen[6] += amount
                newgen[8] += amount
            else:
                newgen[gen-1] += amount

        self.generations = newgen

    def elements(self):
        return list(self.generations.elements())

    def size(self):
        return self.generations.total()

    def __str__(self):
        return f"School({self.generations})"


## Naive approach that did not scale
#class LanternFish:
#    def __init__(self, timer):
#        self.timer = timer
#
#    def spawn(self):
#        if self.timer == 0:
#            self.timer = 6
#            return LanternFish(8)
#        self.timer -=1
#        return
#
#    def __str__(self):
#        return str(self.timer)
#
#    def __repr__(self):
#        return f"LanternFish(timer={self.timer})"
#
#    def copy(self):
#        return LanternFish(self.timer)


def parse_fishes(source):
    return [ int(timer) for timer in source.strip().split(',') ]


def fish_str(fishes):
    return map(str, fishes)


def simulate(fishes, days):
    school = School(fishes)
    debug(f"initial state: {','.join(fish_str(school.elements()))}")

    for i in range(days):
        school.age()
        debug(f"day {i+1: 3d}: {school}")

    return school


def part_one(fishes):
    return simulate(fishes, 80).size()


def part_two(fishes):
    return simulate(fishes, 256).size()


def main():
    fishes = list(chain(*read_input(parse_fishes)))

    print(f"part 1: {part_one(fishes)}")
    print(f"part 2: {part_two(fishes)}")


if __name__ == "__main__":
    main()
