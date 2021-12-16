#!/usr/bin/env python3

from common import read_input, combine, clean
from itertools import pairwise


def differences(measurements):
    return list( b - a for a, b in pairwise(measurements) )


def triple_measures(measurements):
    return list( a + b + c for (a, b), (_, c) in pairwise(pairwise(measurements)) )


def count_increases(measurements):
    return len([x for x in measurements if x > 0])


def part_one(measurements):
    diffs = differences(measurements)

    return count_increases(diffs)


def part_two(measurements):
    triples = triple_measures(measurements)

    diffs = differences(triples)

    return count_increases(diffs)

def main():
    measurements = read_input(combine(int, clean))
    print(f"part 1: {part_one(measurements)}")
    print(f"part 2: {part_two(measurements)}")


if __name__ == "__main__":
    main()
