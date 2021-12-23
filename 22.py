#!/usr/bin/env python3

from common import read_input, combine, clean, debug, color

import re

from dataclasses import dataclass
from collections import defaultdict
from itertools import product, chain, pairwise, tee
from time import time
from datetime import timedelta


def range2str(rng):
    return f"{min(rng)}..{max(rng)}"


@dataclass(frozen=True)
class Cuboid:
    x: list[int]
    y: list[int]
    z: list[int]

    def __iter__(self):
        yield from product(self.x, self.y, self.z)

    def __contains__(self, other):
        match other:
            case Cuboid(_, _, _):
                xl, xh = min(other.x), max(other.x)
                inx = (xh >= min(self.x) and xl <= max(self.x))

                yl, yh = min(other.y), max(other.y)
                iny = (yh >= min(self.y) and yl <= max(self.y))

                zl, zh = min(other.z), max(other.z)
                inz = (zh >= min(self.z) and zl <= max(self.z))

                return inx and iny and inz
            case (x, y, z) | [x, y, z]:
                return x in self.x and y in self.y and z in self.z
            case _:
                return False

    def __str__(self):
        xr = range2str(self.x)
        yr = range2str(self.y)
        zr = range2str(zelf.z)

        return f"Cuboid(x={xr},y={yr},z={zr})"

    def __len__(self):
        return len(self.x) * len(self.y) * len(self.z)


@dataclass(frozen=True)
class LabelledCuboid(Cuboid):
    labels: set[int]

    def __str__(self):
        xr = range2str(self.x)
        yr = range2str(self.y)
        zr = range2str(zelf.z)

        return f"LabelledCuboid(x={xr},y={yr},z={zr},labels={self.labels})"


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

    on = sum( grid[pos] for pos in init_area )

    return on


@dataclass
class Border:
    value: int
    start: int
    idx: int

    def __lt__(self, other):
        return (self.value, self.start, self.idx) < (other.value, other.start, other.idx)


def subdivide_intervals(intervals):
    borders = sorted(
        chain.from_iterable(
            (
                [
                    Border(min(interval), 1, idx),
                    Border(max(interval)+1, 0, idx)
                ] for idx, interval in enumerate(intervals) 
            )
        )
        )

    open_intervals = set()
    max_open = 0

    for a, b in pairwise(borders):
        if a.start:
            open_intervals.add(a.idx)
        else:
            open_intervals.discard(a.idx)

        if len(open_intervals) > max_open:
            max_open = len(open_intervals)

        if len(open_intervals) > 0 and b.value - a.value > 0:
            yield (set(open_intervals), range(a.value, b.value))

    debug(f"max open intervals: {max_open}")

    return


def subdivide_cuboids(cuboids):
    xrs, yrs, zrs = tee(cuboids, 3)

    xrs = subdivide_intervals(map(lambda c: c.x, xrs))
    yrs = subdivide_intervals(map(lambda c: c.y, yrs))
    zrs = subdivide_intervals(map(lambda c: c.z, zrs))

    for xr, yr, zr in product(xrs, yrs, zrs):
        comm = xr[0] & yr[0] & zr[0]
        if len( comm ) > 0:
            yield LabelledCuboid(xr[1], yr[1], zr[1], comm)

    return


def part_two(actions):
    cuboids = subdivide_cuboids(map(lambda a: a.cuboid, actions))
    start = time()

    total = 0
    for idx, cuboid in enumerate(cuboids):
        labels = sorted(cuboid.labels)

        if len(labels) > 0 and actions[labels[-1]].on:
            total += len(cuboid)
            if debug():
                elapsed = timedelta(seconds=time() - start)
                print(f"  {color.FAINT}[{elapsed}]{color.END} {total:>20,} cubes (added {len(cuboid):>15,}) #{idx:,}", end = '\r')

    debug(f"  {total:>20,} cubes! {' '*25}")

    return total


def main():
    actions = read_input(combine(parse_action, clean))

    print(f"part 1: {part_one(actions)}")
    print(f"part 2: {part_two(actions)}")


if __name__ == "__main__":
    main()

