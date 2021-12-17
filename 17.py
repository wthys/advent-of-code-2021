#!/usr/bin/env python3

import re

from common import read_input, clean, combine, Point, sign, color, debug

from dataclasses import dataclass
from collections import defaultdict
from itertools import product
from typing import List


@dataclass(frozen=True)
class Probe:
    position: Point
    velocity: Point

    def move(self):
        pos = self.position + self.velocity
        vel = self.velocity - (sign(self.velocity.x, int), 1)
        return Probe(pos, vel)


@dataclass(frozen=True)
class Area:
    x: range
    y: range

    def __contains__(self, pos):
        return pos.x in self.x and pos.y in self.y

    def __iter__(self):
        return map(lambda pos: Point(*pos), product(self.x, self.y))

    def center(self):
        if len(self.x) == 0 or len(self.y) == 0:
            return None

        xa = sum(self.x) / len(self.x)
        ya = sum(self.y) / len(self.y)
        return Point(xa, ya)


def ensure_pos(pos):
    match pos:
        case Point(_, _):
            return pos
        case (x, y):
            return Point(x, y)
        case [x, y]:
            return Point(x, y)
        case _:
            raise ValueError(f"Could not convert {pos} to Point")


class GridBounds:
    def __init__(self):
        self._tl = None
        self._br = None

    def area(self):
        if self._tl:
            return Area(range(self._tl.x, self._br.x + 1), range(self._tl.y, self._br.y + 1))
        return Area(range(0), range(0))

    def add(self, position):
        pos = ensure_pos(position)

        tl = self._tl
        br = self._br
        if self._tl is None:
            self._tl = pos
            self._br = pos
        else:
            self._tl = Point(min(self._tl.x, pos.x), min(self._tl.y, pos.y))
            self._br = Point(max(self._br.x, pos.x), max(self._br.y, pos.y))


class Grid:
    def __init__(self, grid = None, empty = None):
        if empty is None:
            empty = lambda:None

        self._grid = defaultdict(empty)

        self._bounds = GridBounds()

        if grid:
            self._bounds = (Point(0,0), Point(len(grid[0]), len(grid)))
            for j, row in enumerate(grid):
                for i, value in enumerate(row):
                    self._grid[Point(i,j)] = value
                    self._bounds.add(Point(i,j))


    def area(self):
        return self._bounds.area()

    def set(self, position, value):
        pos = ensure_pos(position)
        self._grid[pos] = value
        self._bounds.add(pos)
        return self

    def get(self, position):
        pos = ensure_pos(position)
        return self._grid[pos]


def print_grid(grid):

    area = grid.area()

    topbot = "+" + "-" * len(area.x) + "+"

    print(topbot)
    for y in reversed(area.y):
        row = ""
        for x in area.x:
            row += str(grid.get((x, y)))
        print(f"|{row}|")
    print(topbot)


def parse_target(line):
    m = re.match(r"target area: x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+)", line)
    if not m:
        return None

    xl, xh, yl, yh = list(map(int, m.group(1,2,3,4)))
    return Area(range(xl, xh + 1), range(yl, yh + 1))


def prepare_grid(start, target_area):
    grid = Grid(empty=lambda:'.')

    grid.set(start, f'{color.RED}S{color.END}')
    for pos in target_area:
        grid.set(pos, f'{color.GREEN}T{color.END}')

    return grid

@dataclass(frozen=True)
class Result:
    success: bool
    probe: Probe
    path: List[Point]
    max_height: int


def simulate_probe(position, velocity, target_area):
    path = [position]

    cot = target_area.center()

    dist_to_target = (cot - position).mag()    

    max_height = position.y

    probe = Probe(position, velocity)
    while probe.position not in target_area:
        probe = probe.move()
        path.append(probe.position)
        max_height = max(max_height, probe.position.y)

        # check we are still moving towards the target
        newdist = (cot - probe.position).mag()
        if probe.velocity.y < 0 and newdist > dist_to_target:
            break

        dist_to_target = newdist

        if probe.position.x > max(target_area.x):
            break


    success = probe.position in target_area
    probe = Probe(position, velocity)
    return Result(success, probe, path, max_height)


def print_result(target_area, result):
    if not debug():
        return

    grid = prepare_grid((0,0), target_area)

    for p in result.path[1:]:
        grid.set(p, f"{color.BLUE}#{color.END}")

    print(f"result: {result.probe}, {result.max_height}")
    print_grid(grid)


def part_one(target_area):

    # first down velocity is 1 more than initial up velocity
    ys = range(max(map(abs, target_area.y)))

    def cond(n):
        return (n * (n + 1) // 2) >= min(target_area.x)

    minx = min(filter(cond, range(min(target_area.x))))
    xs = range(minx, max(target_area.x) + 1)

    best = Result(False, None, None, -10)

    start = Point(0, 0)

    for vx, vy in product(xs, ys):
        result = simulate_probe(start, Point(vx, vy), target_area)
        #print_result(target_area, result)
        if result.success:
            if result.max_height > best.max_height:
                best = result


    if not best.success:
        return "Could not find any solutions T_T"

    print_result(target_area, best)

    calculated = max(ys) * (max(ys) + 1) // 2

    return best.max_height, calculated


def part_two(target_area):
    return 'n/a'


def main():
    content = read_input(combine(parse_target, clean))

    for target in content:
        print(f"part 1: {part_one(target)}")
        print(f"part 2: {part_two(target)}")


if __name__ == "__main__":
    main()
