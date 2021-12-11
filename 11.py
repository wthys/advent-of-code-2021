#!/usr/bin/env python3

from common import read_input, neejbers

from itertools import chain
from collections import defaultdict


def octogrid(octopi):
    grid = {}
    for j, row in enumerate(octopi):
        for i, energy in enumerate(row):
            grid[(i,j)] = energy

    return grid


def is_valid_neejber(x, y, xinterval, yinterval):
    return x in xinterval and y in yinterval


def valid_neejbers(x, y):
    def ivn(pos):
        return is_valid_neejber(pos[0], pos[1], range(10), range(10))

    return list(filter(ivn, neejbers(x, y)))


def step_octopi(octopi):
    # make a copy and increase energy
    grid = { pos: energy+1 for pos, energy in octopi.items() }

    def bursting(energy):
        return energy >= 10

    flashers = set()

    def bursters(grid):
        return list(filter(lambda pos: bursting(grid[pos]) and pos not in flashers, grid))

    # FLASH! AAAaaa!
    while len(bursters(grid)) > 0:
        ngrid = { pos: energy for pos, energy in grid.items() }
        for i, j in bursters(grid):
            flashers.add((i, j))
            for x, y in valid_neejbers(i, j):
                ngrid[(x, y)] += 1

        grid = ngrid

    # drain the energy of the flashers
    for i, j in flashers:
        grid[(i, j)] = 0

    return grid, len(flashers)


def part_one(octopi):
    grid = octogrid(octopi)

    total = 0
    for _ in range(100):
        grid, flashes = step_octopi(grid)
        total += flashes

    return total


def part_two(octopi):
    return 'n/a'


def parse_line(line):
    return list(map(int, line.strip()))


def main():
    octopi = read_input(parse_line)
    print(f"part1: {part_one(octopi)}")
    print(f"part2: {part_two(octopi)}")


if __name__ == "__main__":
    main()
