#!/usr/bin/env python3

from common import debug, read_input, neejbers, combine, intlist, clean, color

import operator

from collections import defaultdict
from itertools import product, chain


class HeightMap:
    def __init__(self, height_map):
        self.height_map = defaultdict(lambda : 100)
        self._size = (len(height_map[0]), len(height_map))

        for j, row in enumerate(height_map):
            for i, height in enumerate(row):
                self.height_map[(i,j)] = height

    def size(self):
        return self._size[:]


    def height(self, x, y):
        return self.height_map[(x, y)]


    def find_lower(self, x, y):
        threshold = self.height(x, y)

        def check_lower(i, j):
            return self.height(i, j) <= threshold
        
        return self.find_neejbers(x, y, check_lower)


    def find_higher(self, x, y):
        threshold = self.height(x, y)

        def check_higher(i, j):
            h = self.height(i, j)
            return h >= threshold and h < 9

        return self.find_neejbers(x, y, check_higher)


    def find_neejbers(self, x, y, func):
        def ffunc(pos):
            return func(*pos)

        def valid(pos):
            return pos[0] in range(self._size[0]) and pos[1] in range(self._size[1])

        return list(filter(ffunc, filter(valid, neejbers(x, y, diagonal=False))))


    def find_minima(self):

        def is_lowest(pos):
            return len(self.find_lower(*pos)) == 0

        # not directly over keys because find_lower seems to modify the dict
        return set(filter(is_lowest, list(self.height_map.keys())))


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


def print_heightmap(heightmap, poi = None):
    if not debug():
        return

    dims = heightmap.size()
    topbot = "+" + "-" * dims[0] + "+"
    print(topbot)
    for j in range(dims[1]):
        row = ""
        for i in range(dims[0]):
            h = heightmap.height(i, j)
            if poi and (i, j) in poi:
                row += f"{color.RED}{color.FAINT}{h}{color.END}"
            else:
                row += f"{h}"
        print(f"|{row}|")
    print(topbot)


def part_one(readings):
    hmap = HeightMap(readings)

    minima = hmap.find_minima()

    print_heightmap(hmap, minima)

    return sum( hmap.height(*pos)+1 for pos in minima )


def part_two(readings):
    hmap = HeightMap(readings)

    basins = hmap.find_basins()

    basin_sizes = list(sorted(map(len, basins)))

    print_heightmap(hmap, set(chain(*basins)))

    return basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]


def main():
    readings = read_input(combine(intlist, clean))

    print(f"part 1: {part_one(readings)}")
    print(f"part 2: {part_two(readings)}")


if __name__ == "__main__":
    main()
