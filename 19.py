#!/usr/bin/env python3

from common import read_input, clean, color, debug, ident, combine

import re
import math

from dataclasses import dataclass
from collections import defaultdict
from itertools import chain, combinations, product


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
        return abs(self.x) + abs(self.y) + abs(self.z)

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
            continue

        m = re.match(r"(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)", line)
        if m:
            x, y, z = m.group(1,2,3)
            cur_bcns.append(Point3(int(x), int(y), int(z)))
            continue

        scanners.append(Scanner(cur_id, cur_bcns))
        cur_id = None
        cur_bcns = None

    if cur_id:
        scanners.append(Scanner(cur_id, cur_bcns))

    return scanners


class Signature:
    def __init__(self, points):
        ordered = sorted(points, key=lambda p: (p.x, p.y, p.z))
        if len(ordered) < 2:
            raise ValueError(f"Signature needs at least two points")

        self._nexus = ordered[0]
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

    def nexus(self):
        return self._nexus


def find_match(known, candidate):
    n = 0
    known_beacons = set(known.beacons)
    for cand in map(lambda rot: candidate.rotate(rot), rotations()):
        for trans in set( c - k for k, c in product(known.beacons, cand.beacons) ):
            n += 1
            if debug():
                print(f"  {color.FAINT}checking ({trans.x:>+5d},{trans.y:>+5d},{trans.z:>+5d}) /{n:<6d}{color.END}", end = '\r')
            suspects = set(map(lambda b: b - trans, cand.beacons))

            common = known_beacons & suspects
            if len(common) >= 12:
                home = Signature(common)
                dest = Signature(map(lambda b: b + trans, common))

                found = cand.with_coord(home.nexus() - dest.nexus())
                debug(f"  {color.RED}MATCH FOUND{color.END} - {known} -- {found}")
                return found

    return None


def part_one(scanners):

    scanmap = { s.id: s for s in scanners }

    known = scanmap[0]
    del scanmap[0]

    found = [known]

    while len(scanmap) > 0:
        for scanid, scanner in list(scanmap.items()):
            match = find_match(known, scanner)
            if match:
                known = Scanner(0, set(chain(known, match)))
                del scanmap[scanid]
                found.append(match)
                break

    debug(f"known world contained by {known}")

    return len(list(known))


def part_two(scanners):
    return 'n/a'


def main():
    content = read_input(clean)

    scanners = parse_input(content)

    scanmap = { s.id: s for s in scanners }

    known = scanmap[0]
    del scanmap[0]

    found = [known]

    while len(scanmap) > 0:
        debug(f"Scanners left: {len(scanmap):>3d} / {' '.join(map(str, scanmap))}")
        for scanid, scanner in list(scanmap.items()):
            match = find_match(known, scanner)
            if match:
                known = Scanner(0, set(chain(known, match)))
                del scanmap[scanid]
                found.append(match)
                break

    debug(f"known world contained by {known}")

    print(f"part 1: {len(list(known))}")


    largest_dist = 0

    for a, b in combinations(found, 2):
        dist = (a.coord - b.coord).mag()
        if dist > largest_dist:
            debug(f"  {color.GREEN}NEW RECORD{color.END} : {dist} between {a.id} and {b.id}")
            largest_dist = dist


    print(f"part 2: {largest_dist}")


if __name__ == "__main__":
    main()


