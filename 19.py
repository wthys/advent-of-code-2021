#!/usr/bin/env python3

from common import read_input, clean, color, debug, sign, ident, combine

import re
import math

from dataclasses import dataclass
from numbers import Real, Integral
from collections import Counter
from itertools import combinations, permutations, product


def ensure_number(n, msg=None):
    if isinstance(n, Real):
        return n
    if msg:
        raise ValueError(msg)
    raise ValueError(f"{n} is not a number")

def ensure_int(n, msg=None):
    if isinstance(n, Integral):
        return n
    if int(n) == n:
        return int(n)
    if msg:
        raise ValueError(msg)
    raise ValueError(f"{n} is not an integer")


@dataclass(frozen=True)
class Point3:
    x: int
    y: int
    z: int

    def __sub__(self, other):
        return self + (-other)

    def __add__(self, other):
        match other:
            case Point3(x, y, z) | (x, y, z) | [x, y, z]:
                return Point3(self.x + x, self.y + y, self.z + z)
            #case (x, y, z):
            #    return Point3(self.x - x, self.y - y, self.z - z)
            #case [x, y, z]:
            #    return Point3(self.x - x, self.y - y, self.z - z)
            case _:
                raise ValueError(f"Cannot add {type(other)} to {self.__class__.__name__}")

    def __neg__(self):
        return Point3(-self.x, -self.y, -self.z)

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def __repr__(self):
        return f"Point3{self}"


def rotx(p):
    return Point3( p.x, -p.z,  p.y)

def roty(p):
    return Point3( p.z,  p.y, -p.x)

def rotz(p):
    return Point3(-p.y,  p.x,  p.z)

def rotations():
    yield ident
    yield rotx
    yield combine(rotx, rotx)
    yield combine(rotx, rotx, rotx)

    yield                           rotz
    yield combine(roty,             rotz)
    yield combine(roty, roty,       rotz)
    yield combine(roty, roty, roty, rotz)

    yield combine(                  rotz, rotz)
    yield combine(rotx,             rotz, rotz)
    yield combine(rotx, rotx,       rotz, rotz)
    yield combine(rotx, rotx, rotx, rotz, rotz)

    yield combine(                  rotz, rotz, rotz)
    yield combine(roty,             rotz, rotz, rotz)
    yield combine(roty, roty,       rotz, rotz, rotz)
    yield combine(roty, roty, roty, rotz, rotz, rotz)

    yield                           roty
    yield combine(rotz,             roty)
    yield combine(rotz, rotz,       roty)
    yield combine(rotz, rotz, rotz, roty)

    yield combine(                  roty, roty, roty)
    yield combine(rotz,             roty, roty, roty)
    yield combine(rotz, rotz,       roty, roty, roty)
    yield combine(rotz, rotz, rotz, roty, roty, roty)


@dataclass(frozen=True)
class Scanner:
    id: int
    beacons: list[Point3]
    coord: Point3 = Point3(0,0,0)

    def with_coord(self, coord):
        return Scanner(self.id, self.beacons[:], coord)

    def __iter__(self):
        yield from map(lambda p: self.coord + p, self.beacons)

    def rotate(self, rot):
        return Scanner(self.id, list(map(rot, self.beacons)), self.coord)

    def __str__(self):
        return f"Scanner(id={self.id}, bcns={len(self.beacons)}, coord={self.coord})"

"""
How to find overlaps?

- point structure will be the same for the overlap
    - match on pair vectors?
"""


def parse_input(content):
    scanners = []

    cur_id = None
    cur_bcns = None

    for line in content:
        m = re.match(r"--- scanner ([0-9]+) ---", line)
        if m:
            cur_id = int(m.group(1))
            cur_bcns = []
            debug(f"-- found scanner {cur_id}")
            continue

        m = re.match(r"(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)", line)
        if m:
            x, y, z = m.group(1,2,3)
            cur_bcns.append(Point3(int(x), int(y), int(z)))
            debug(f"  -- found beacon {cur_bcns[-1]}")
            continue

        scanners.append(Scanner(cur_id, cur_bcns))
        cur_id = None
        cur_bcns = None

    if cur_id:
        scanners.append(Scanner(cur_id, cur_bcns))

    return scanners


class Signature:
    def __init__(self, points):
        if len(points) < 2:
            raise ValueError(f"Signature needs at least two points")

        ordered = sorted(points, key=lambda p: (p.x, p.y, p.z))
        self._nexus = ordered[0]
        self._points = ordered
        self._signature = list(map(lambda p: p - self._nexus, ordered[1:]))

    def __eq__(self, other):
        if not isinstance(other, Signature):
            return False

        if len(self._signature) != len(other._signature):
            return False

        for l, r in zip(self._signature, other._signature):
            if l != r:
                return False

        return True

    def rotate(self, rot):
        return Signature(list(map(rot, self._points)))

    def nexus(self):
        return self._nexus


def find_overlaps(known, candidate):
    n = 0
    for truth in map(Signature, combinations(known.beacons, 12)):
        for prospect in map(Signature, combinations(candidate.beacons, 12)):
            for rot in rotations():
                n += 1
                if debug():
                    print(f"{color.FAINT}checking #{n:<10d}{color.END}", end = "\r")
                if truth == prospect.rotate(rot):
                    debug(f"{color.RED}FOUND MATCH{color.END}  {known} -> {candidate}")
                    yield (truth, prospect.rotate(rot), rot)


def part_one(scanners):

    debug(f"scanners: {', '.join(map(str, scanners))}")

    scanmap = { s.id: s for s in scanners }

    root = scanmap[0]

    for overlap in find_overlaps(root, scanmap[1]):
        nexusA = overlap[0].nexus()
        nexusB = overlap[1].nexus()

        matching = scanmap[1].rotate(overlap[2]).with_coord(nexusA - nexusB)
        debug(f"{root} -> {matching}")








    

    return 'n/a'


def part_two(scanners):
    return 'n/a'


def main():
    content = read_input(clean)

    scanners = parse_input(content)

    print(f"part 1: {part_one(scanners)}")
    print(f"part 2: {part_two(scanners)}")


if __name__ == "__main__":
    main()


