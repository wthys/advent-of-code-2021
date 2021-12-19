#!/usr/bin/env python3

from common import read_input, clean, color, debug, sign

import re
import math

from dataclasses import dataclass
from numbers import Real, Integral
from sortedcontainers import SortedList
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
        return self + (other * -1)

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

    def __mul__(self, other):
        ensure_number(other, f"Cannot multiply {self.__class__.__name__} with {type(other)}")
        return Point3(self.x * other, self.y * other, self.z * other)


    def __mod__(self, other):
        match other:
            case Point3(x, y, z) | (x, y, z) | [x, y, z]:
                return Point3(self.x % x, self.y % y, self.z % z)
            case _:
                n = ensure_number(other, "Cannot modulo {self.__class__.__name__} with {type(other)}")
                return Point3(self.x % n, self.y % n, self.z % n)


    def rotate90(self, x=None, y=None, z=None):
        x = 0 if x is None else (ensure_int(x) % 4)
        y = 0 if y is None else (ensure_int(y) % 4)
        z = 0 if z is None else (ensure_int(z) % 4)

        if x:
            return Point3(self.x, -self.z, self.y).rotate90(x - 1, y, z)
        if y:
            return Point3(self.z, self.y, -self.x).rotate90(x, y - 1, z)
        if z:
            return Point3(-self.y, self.x, self.z).rotate90(x, y, z - 1)
        return self

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def __repr__(self):
        return f"Point3{self}"

@dataclass(frozen=True)
class Scanner:
    id: int
    beacons: list[Point3]
    rotation: Point3 = Point3(0,0,0)

    def rotate90(self, x = None, y = None, z = None):
        x = 0 if x is None else (ensure_int(x) % 4)
        y = 0 if y is None else (ensure_int(y) % 4)
        z = 0 if z is None else (ensure_int(z) % 4)

        bcns = map(lambda b: b.rotate90(x, y, z), self.beacons)
        rot = (self.rotation + (x, y, z)) % 4
        return Scanner(self.id, list(bcns), rot)

    def translate(self, vector):
        bcns = map(lambda b: b + vector, self.beacons)
        return Scanner(self.id, list(bcns), self.rotation)

    def __str__(self):
        return f"Scanner(id={self.id}, rot={self.rotation}, bcns={len(self.beacons)})"


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


@dataclass(frozen=True)
class Overlap:
    beacons: list[Point3]
    structure: Counter[Point3]
    rotation: Point3 = Point3(0,0,0)

    def __eq__(self, other):
        return self.structure == other.structure


def find_plane(p1, p2, p3):

    d1 = p2 - p1
    d2 = p3 - p1

    a = d1.y * d2.z - d2.x * d1.z
    b = d2.x * d1.z - d1.x * d2.z
    c = d1.x * d2.y - d2.x * d1.y
    d = (-a * p1.x - b * p1.y - c * p1.z)

    def in_plane(p):
        return (a * p.x + b * p.y + c * p.z + d) == 0

    return in_plane

def create_subsets(scanner):
    for beacons in combinations(scanner.beacons, 12):
        in_plane = find_plane(*(beacons[:3]))
        if sum(1 for _ in filter(in_plane, beacons)) == len(beacons):
            continue
        
        structure = Counter( a - b for a, b in permutations(beacons, 2) )
        yield Overlap(beacons, structure, scanner.rotation)


def find_overlaps(source, target):

    n = 0

    for tgt_overlap in create_subsets(target):
        for x, y, z in product(range(-1, 3), repeat=3):
            for src_overlap in create_subsets(source.rotate90(x, y, z)):
                n += 1

                if debug():
                    print(f"  checking #{n: 5d}     ", end="\r")
                if tgt_overlap == src_overlap:
                    yield (src_overlap, tgt_overlap)
    

    debug(f"  done checking!            ")


def part_one(scanners):

    debug(f"scanners: {', '.join(map(str, scanners))}")

    root = list(filter(lambda s: s.id == 0, scanners))[0]

    first = None
    fixed = [root]
    links = []
    newfixed = []
    for target in fixed:
        for candidate in filter(lambda s: s.id not in set( x.id for x in fixed ), scanners):
            for overlap in find_overlaps(candidate, target):
                rot = overlap[0].rotation
                cand = candidate.rotate90(rot.x, rot.y, rot.z)
                newfixed.append(cand)
                links.append((cand, overlap, target))

    if debug(f"found {len(links)} overlaps:"):
        for node, overlap, root in links:
            debug(f"{node} -> {root}")







    

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


