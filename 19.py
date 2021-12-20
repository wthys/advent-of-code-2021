#!/usr/bin/env python3

from common import read_input, clean, color, debug, ident, combine

import re
import math

import multiprocessing as mp

from dataclasses import dataclass
from itertools import chain, combinations, product
from time import time


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
    # rotate around +x/1
    yield ident
    yield rotx
    yield combine(rotx, rotx)
    yield combine(rotx, rotx, rotx)

    # rotate around +y/2
    yield                           rotz
    yield combine(roty,             rotz)
    yield combine(roty, roty,       rotz)
    yield combine(roty, roty, roty, rotz)

    # rotate around -x/6
    yield combine(                  rotz, rotz)
    yield combine(rotx,             rotz, rotz)
    yield combine(rotx, rotx,       rotz, rotz)
    yield combine(rotx, rotx, rotx, rotz, rotz)

    # rotate around -y/5
    yield combine(                  rotz, rotz, rotz)
    yield combine(roty,             rotz, rotz, rotz)
    yield combine(roty, roty,       rotz, rotz, rotz)
    yield combine(roty, roty, roty, rotz, rotz, rotz)

    # rotate around -z/4
    yield                           roty
    yield combine(rotz,             roty)
    yield combine(rotz, rotz,       roty)
    yield combine(rotz, rotz, rotz, roty)

    # rotate around +z/3
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


def find_match(known, candidate):
    """
    Find a match by going over all possible translations between the known
    beacon coordinates and the suspected coordinates (after rotation). If
    twelve or more suspected coordinates map to known coordinates using a
    transision, we assume that is the wanted transition and we can return the
    rotated candidate with a filled in coordinate based on the known world.

    Thanks Timmy for the tip on this part! ❤
    """
    n = 0
    known_beacons = set(known.beacons)

    # make sure we go over all rotations
    for cand in map(lambda rot: candidate.rotate(rot), rotations()):

        # try to map the unknown points to the known world so `c - trans = k`
        for trans in set( c - k for k, c in product(known.beacons, cand.beacons) ):
            n += 1
            
            suspects = set(map(lambda s: s - trans, cand.beacons))

            common = known_beacons & suspects
            if len(common) >= 12:
                """
                The points in `common` are the same in both coordinate systems.
                To get the coordinate for the unknown scanner, we know that we
                have to go from root -> common point -> unknown

                    # take the common point in known coordinate, e.g.
                    # root->common point
                    home = common[0]

                    # restore dest to foreign coordinate, e.g. unknown ->
                    # common point
                    dest = home + trans
                    
                    # dest points away from the unknown scanner so reverse it
                    # and add it to home... turns out we didn't need to do
                    # these calculations!
                    coord = home - dest
                          = home - home - trans
                          = -trans
                """
                found = cand.with_coord( -trans )
                debug(f"  {color.RED}MATCH FOUND{color.END} - {known.id} -- {found.id} @ {found.coord} #{n}")
                return (candidate.id, found)

    return (candidate.id, None)


def main():
    start = time()
    content = read_input(clean)

    scanners = parse_input(content)

    scanmap = { s.id: s for s in scanners }

    known = scanmap[0]
    del scanmap[0]

    found = [known]


    def print_progress():
        if debug():
            since = f"{time() - start:.3f}s"
            s_timing = f"{color.FAINT}[{since:>10}]{color.END}"

            s_done = color.GREEN + color.FAINT + (' '.join(map(lambda s: str(s.id), found))) + color.END
            s_left = ' '.join(map(str, scanmap))

            print(f"{s_timing} Progress: {s_done} | {s_left}") 

    debug(f"using {mp.cpu_count()} processors...")

    while len(scanmap) > 0:
        print_progress()

        with mp.Pool(mp.cpu_count()) as pool:

            results = [ pool.apply(find_match, args=(known, scanner)) for scanner in scanmap.values() ]
            pool.close()
            pool.join()

            for scanid, match in results:
                debug(f"found result #{scanid} = {match}")
                if match:
                    known = Scanner(0, set(chain(known, match)))
                    del scanmap[scanid]
                    found.append(match)

    print_progress()

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


