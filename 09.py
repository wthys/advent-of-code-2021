#!/usr/bin/env python3

from common import read_input

import operator

from collections import defaultdict
from itertools import product, chain


class HeightMap:
    def __init__(self, height_map):
        self.height_map = defaultdict(lambda : 100)
        for i, row in enumerate(height_map):
            for j, height in enumerate(row):
                self.height_map[(i,j)] = height


    def height(self, x, y):
        return self.height_map[(x,y)]


    def find_lower(self, x, y):
        threshold = self.height(x, y)
        
        return self.find_neejbers(x, y, lambda i, j: self.height(i, j) < threshold)


    def find_higher(self, x, y):
        threshold = self.height(x, y)

        return self.find_neejbers(x, y, lambda i, j: self.height(i, j) >= threshold and self.height(i, j) < 9)


    def find_neejbers(self, x, y, func):
        neejbers = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]

        found = []
        for (i, j) in neejbers:
            if func(i, j):
                found += [(i, j)]

        return found


    def find_minima(self):
        minima = []
        for (x, y) in list(self.height_map.keys()):
            if len(self.find_lower(x, y)) == 0:
                minima += [(x, y)]

        return minima


    def find_basins(self):
        minima = self.find_minima()

        basins = []
        
        for minimum in minima:
            basin = set([minimum])

            while True:
                higher = set(chain(*[ self.find_higher(x, y) for (x, y) in basin ])) - basin

                if len(higher) == 0:
                    break

                basin |= higher

            basins.append(basin)

        return basins



def parse_line(source):
    return [ int(x) for x in source.strip() ]


def part_one(readings):
    hmap = HeightMap(readings)

    minima = hmap.find_minima()

    return sum( hmap.height(*pos)+1 for pos in minima )


def part_two(readings):
    hmap = HeightMap(readings)

    basins = hmap.find_basins()

    basin_sizes = list(sorted(map(len, basins)))

    return basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]


def main():
    readings = read_input(parse_line)

    print(f"part1: {part_one(readings)}")
    print(f"part2: {part_two(readings)}")


if __name__ == "__main__":
    main()
