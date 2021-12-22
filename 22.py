#!/usr/bin/env python3

from common import read_input, combine, clean, debug, color

import re

from dataclasses import dataclass
from collections import defaultdict
from itertools import product
from time import time



@dataclass(frozen=True)
class Cuboid:
    x: list[int]
    y: list[int]
    z: list[int]

    def __iter__(self):
        yield from product(self.x, self.y, self.z)

    def __contains__(self, pos):
        match pos:
            case Cuboid(_, _, _):
                xl, xh = min(pos.x), max(pos.x)
                inx = (xh >= min(self.x) and xl <= max(self.x))

                yl, yh = min(pos.y), max(pos.y)
                iny = (yh >= min(self.y) and yl <= max(self.y))

                zl, zh = min(pos.z), max(pos.z)
                inz = (zh >= min(self.z) and zl <= max(self.z))

                return inx and iny and inz
            case (x, y, z) | [x, y, z]:
                return x in self.x and y in self.y and z in self.z
            case _:
                return False

    def __str__(self):
        return f"Cuboid(x={min(self.x)}..{max(self.x)},y={min(self.y)}..{max(self.y)},z={min(self.z)}..{max(self.z)})"


@dataclass(frozen=True)
class Action:
    on: bool
    cuboid: Cuboid

    def apply(self, grid, init_area = None):
        if init_area:
            if not(self.cuboid in init_area):
                return 0

        n = 0
        for pos in filter(lambda pos: pos in init_area, self.cuboid):
            state = grid[pos]
            if state != self.on:
                grid[pos] = self.on
                n += 1
        return n

def parse_action(line):
    m = re.match(r"(on|off) x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+)", line)

    if m:
        on = m.group(1) == "on"
        xl, xh = sorted(list(map(int, m.group(2, 3))))
        yl, yh = sorted(list(map(int, m.group(4, 5))))
        zl, zh = sorted(list(map(int, m.group(6, 7))))

        return Action(on, Cuboid(range(xl, xh + 1), range(yl, yh + 1), range(zl, zh + 1)))

    raise ValueError(f"Could not make sense of `{line}`")


def part_one(actions):
    grid = defaultdict(lambda:False)

    init_area = Cuboid(range(-50, 51), range(-50, 51), range(-50, 51))

    for action in actions:
        n = action.apply(grid, init_area)
        debug(f"made {n} change with {action}")

    on = sum( grid[pos] for pos in init_area )

    return on


def part_two(actions):
    return 'n/a'


def main():
    actions = read_input(combine(parse_action, clean))

    print(f"part 1: {part_one(actions)}")
    print(f"part 2: {part_two(actions)}")


if __name__ == "__main__":
    main()

