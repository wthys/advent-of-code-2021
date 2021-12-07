#!/usr/bin/env python3

from itertools import chain

from common import read_input


def parse_crabs(source):
    return [ int(pos) for pos in source.strip().split(',') ]



def simple_engine(dist):
    return dist


def crab_engine(dist):
    return  dist * (dist + 1) // 2


def fuel_cost(crabs, pos, engine):
    return sum( engine(abs(crab - pos)) for crab in crabs )


def find_cheapest(crabs, engine):
    cheapest = None
    for pos in range(min(crabs), max(crabs)+1):
        cost = fuel_cost(crabs, pos, engine)
        #print(f"pos {pos: 3d}: {cost: 4d} fuel")
        if cheapest is None or cheapest[1] > cost:
            cheapest = (pos, cost)

    print(f"cheapest position: {cheapest[0]} for {cheapest[1]} fuel")

    return cheapest

def part_one(crabs):
    cheapest = find_cheapest(crabs, simple_engine)
    return cheapest[1]


def part_two(crabs):
    cheapest = find_cheapest(crabs, crab_engine)
    return cheapest[1]
    

def main():
    crabs = list(chain(*read_input(parse_crabs)))

    print(f"part1: {part_one(crabs)}")
    print(f"part2: {part_two(crabs)}")


if __name__ == "__main__":
    main()
