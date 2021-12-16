#!/usr/bin/env python3

import re

from collections import namedtuple, Counter
from functools import cache
from itertools import chain

from common import debug, read_input, Point, interpolate_points, color


class Vent:
    def __init__(self, start, end):
        self.start = start
        self.end = end


    @cache
    def is_horizontal(self):
        return self.start.x == self.end.x


    @cache
    def is_vertical(self):
        return self.start.y == self.end.y


    @cache
    def is_diagonal(self):
        return not( self.is_vertical() or self.is_horizontal() )


    def interpoints(self):
        return interpolate_points(self.start, self.end)


    def __str__(self):
        return f"Vent({self.start}, {self.end})"


class SeaFloor:
    def __init__(self, vents):
        self.vents = vents[:]

    def danger_zones(self, threshold=None, diagonals=None):
        if threshold is None:
            threshold = 1

        locations = Counter()
        if diagonals is None or not diagonals:
            for vent in self.vents:
                if vent.is_diagonal():
                    continue
                points = vent.interpoints()
                locations.update(points)
        else:
            for vent in self.vents:
                points = vent.interpoints()
                locations.update(points)

        return [ loc for loc in locations if locations[loc] >= threshold ]


def parse_vent(source):
    m = re.match(r"(?P<sx>[0-9]+),(?P<sy>[0-9]+)\s*->\s*(?P<ex>[0-9]+),(?P<ey>[0-9]+)", source.strip())

    if m is None:
        raise ValueError(f""""Could not parse "{source.strip()}".""")

    sx, sy, ex, ey = m.group('sx', 'sy', 'ex', 'ey')

    return Vent(Point(int(sx), int(sy)), Point(int(ex), int(ey)))


def print_seafloor(sea_floor, poi = None):
    if not debug():
        return

    xs = list(chain(*[(v.start.x, v.end.x) for v in sea_floor.vents]))
    ys = list(chain(*[(v.start.y, v.end.y) for v in sea_floor.vents]))

    dims = ( Point(min(xs), min(ys)), Point(max(xs), max(ys)) )

    diff = dims[1] - dims[0]

    grid = []
    for j in range(dims[0].y, dims[1].y + 1):
        grid.append( list("." * (diff.x + 1)) )

    if poi:
        for p in poi:
            rel = p - dims[0]
            grid[rel.y][rel.x] = f"{color.RED}{color.BOLD}X{color.END}"

    topbot = "+" + "-" * (diff.x + 1) + "+"
    print(topbot)
    for row in grid:
        print(f"|{''.join(row)}|")
    print(topbot)


def part_one(vents):
    sea_floor = SeaFloor(vents)

    dzs = sea_floor.danger_zones(threshold=2, diagonals=False)

    print_seafloor(sea_floor, dzs)

    return len(dzs)


def part_two(vents):
    sea_floor = SeaFloor(vents)

    dzs = sea_floor.danger_zones(threshold=2, diagonals=True)

    print_seafloor(sea_floor, dzs)

    return len(dzs)


def main():
    vents = read_input(parse_vent)

    print(f"part 1: {part_one(vents)}")
    print(f"part 2: {part_two(vents)}")


if __name__ == "__main__":
    main()
