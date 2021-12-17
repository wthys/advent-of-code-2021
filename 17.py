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

    def path(self, stop=None):
        if stop is None:
            stop = lambda _ : False

        yield self.position

        probe = self.move()
        while not stop(probe):
            yield probe.position
            probe = probe.move()

        yield probe.position

    def __repr__(self):
        return f"Probe({repr(self.position)},{repr(self.velocity)})"


@dataclass(frozen=True)
class Area:
    x: range
    y: range

    def __contains__(self, pos):
        return pos.x in self.x and pos.y in self.y

    def __iter__(self):
        return map(lambda pos: Point(*pos), product(self.x, self.y))


def parse_target(line):
    m = re.match(r"target area: x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+)", line)
    if not m:
        return None

    xl, xh, yl, yh = list(map(int, m.group(1,2,3,4)))
    return Area(range(xl, xh + 1), range(yl, yh + 1))


@dataclass(frozen=True)
class Result:
    success: bool
    probe: Probe
    path: List[Point]
    max_height: int


def simulate_probe(probe, target_area):
    def stop(p):
        pos = p.position
        return pos in target_area or pos.x > max(target_area.x) or pos.y < min(target_area.y)

    path = list(probe.path(stop))
    success = path[-1] in target_area
    max_height = max( p.y for p in path )

    return Result(success, probe, path, max_height)


def print_result(result):
    debug(f"result: {result.probe}, {result.max_height}")


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
        probe = Probe(start, Point(vx, vy))
        result = simulate_probe(probe, target_area)
        #print_result(result)
        if result.success:
            if result.max_height > best.max_height:
                best = result


    if not best.success:
        return "Could not find any solutions T_T"

    print_result(best)

    return best.max_height


def part_two(target_area):

    ys = range(min(target_area.y), max(map(abs, target_area.y)))

    def cond(n):
        return (n * (n + 1) // 2) >= min(target_area.x)

    minx = min(filter(cond, range(min(target_area.x))))
    xs = range(minx, max(target_area.x) + 1)

    results = []
    start = Point(0, 0)

    for vx, vy in product(xs, ys):
        probe = Probe(start, Point(vx, vy))
        result = simulate_probe(probe, target_area)

        if result.success:
            results.append(result)

    velocities = set(map(lambda r: r.probe.velocity, results))

    return len(velocities)


def main():
    content = read_input(combine(parse_target, clean))

    for target in content:
        print(f"part 1: {part_one(target)}")
        print(f"part 2: {part_two(target)}")


if __name__ == "__main__":
    main()
