#!/usr/bin/env python3

from common import read_input, combine, clean, debug, color

import re
import heapq

from dataclasses import dataclass
from collections import defaultdict
from itertools import product, chain, pairwise, tee
from time import time


def split_range(orig, intruder):
    """
    orig:     olo                               ohi
               |----------|-------------|--------|
    intruder:            ilo           ihi


    left:   olo -> min(ilo,ohi), e.g. empty when ilo <= olo
    right:  max(olo, ihi) -> ohi, e.g. empty when ihi >= ohi
    middle: min(ilo, ohi) -> max(ihi, olo), e.g. empty when
    """
    olo, ohi = min(orig), max(orig)
    ilo, ihi = min(intruder), max(intruder)

    if ohi < ilo:
        return orig, range(0), range(0)
    elif olo > ihi:
        return range(0), range(0), orig

    return (
            range(olo,           min(ilo, ohi)),
            range(min(ilo, ohi), max(ihi, olo)),
            range(max(ilo, ohi), ohi),
            )


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

    def __len__(self):
        return len(self.x) * len(self.y) * len(self.z)

    def __and__(self, other):
        if self not in other:
            return Cuboid(range(0), range(0), range(0))
        oxl, oxh = min(other.x), max(other.x)
        oyl, oyh = min(other.y), max(other.y)
        ozl, ozh = min(other.z), max(other.z)

        xl, xh = min(self.x), max(self.x)
        yl, yh = min(self.y), max(self.y)
        zl, zh = min(self.z), max(self.z)

        xr = range(max(xl, oxl), min(xh, oxh))
        yr = range(max(yl, oyl), min(yh, oyh))
        zr = range(max(zl, ozl), min(zh, ozh))

        return Cuboid(xr, yr, zr)

    def __le__(self, other):
        oxl, oxh = min(other.x), max(other.x)
        oyl, oyh = min(other.y), max(other.y)
        ozl, ozh = min(other.z), max(other.z)

        xl, xh = min(self.x), max(self.x)
        yl, yh = min(self.y), max(self.y)
        zl, zh = min(self.z), max(self.z)

        return (oxl <= xl and xh <= oxh) and (oyl <= yl and yh <= oyh) and (ozl <= zl and zh <= ozh)




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


@dataclass
class Border:
    value: int
    start: bool
    idx: int

def subdivide_intervals(intervals):
    borders = sorted(
        chain.from_iterable(
            (
                [
                    Border(min(interval), True, idx),
                    Border(max(interval)+1, False, idx)
                ] for idx, interval in enumerate(intervals) 
            )
        ),
        key=lambda b: (b.value, [0,1][b.start])
        )

    #borders = heapq.merge(
    #        *map(
    #            lambda cpl: [
    #                Border(min(cpl[1]), True, cpl[0]),
    #                Border(max(cpl[1]), False, cpl[0])
    #                ],
    #            enumerate(intervals)
    #        ),
    #        key = lambda b: (b.value, [0,1][b.start])
    #        )

    open_intervals = set()

    for a, b in pairwise(borders):
        if a.start:
            open_intervals.add(a.idx)
        else:
            open_intervals.discard(a.idx)

        if a.value != b.value:
            yield (set(open_intervals), range(a.value, b.value))

    return


def subdivide_cuboids(cuboids, remove=None, n=None):

    cubs = cuboids
    if remove:
        cubs = chain([remove], cuboids)

    xrs, yrs, zrs = tee(cubs, 3)

    xrs = subdivide_intervals(map(lambda c: c.x, xrs))
    yrs = subdivide_intervals(map(lambda c: c.y, yrs))
    zrs = subdivide_intervals(map(lambda c: c.z, zrs))

    #xrs, yrs, zrs = zip(*map(lambda c: (c.x, c.y, c.z),cubs))
    debug(f"{n}")
    #try:
    #    debug(f"#n={n}, xrs={len(xrs)}, #yrs={len(yrs)}, #zrs={len(zrs)}")
    #except TypeError:
    #    pass


    nn = 0

    for xr, yr, zr in product(xrs, yrs, zrs):
        nn += 1
        comm = xr[0] & yr[0] & zr[0]
        if len( comm ) > 0 and not( 0 in comm ):
            if debug():
                print(f"  {n}: {nn}  ", end='\r')
            yield Cuboid(xr[1], yr[1], zr[1])

    return

    
    


def part_two(actions):

    total = 0

    for idx, action in enumerate(actions):
        if action.on:
            removed = set()
            for future_action in actions[idx+1:]:
                if action.cuboid in future_action.cuboid:
                    if action.cuboid <= future_action.cuboid:
                        break
                    # no difference in on or off, on will be counted with the
                    # next iteration, off will be removed anyway
                    for p in (action.cuboid & future_action.cuboid):
                        points.discard(p)
        debug(f"  {idx:>3} {action} : {total:,} points")

    return total



def main():
    actions = read_input(combine(parse_action, clean))

    print(f"part 1: {part_one(actions)}")
    print(f"part 2: {part_two(actions)}")


if __name__ == "__main__":
    main()
