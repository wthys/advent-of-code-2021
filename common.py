#!/usr/bin/env python3

import fileinput
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])


def ident(something):
    return something


def read_input(transform = None):
    if transform is None:
        transform = ident

    with fileinput.input() as content:
        return [ transform(line) for line in content ]


def sign(value):
    if value == 0:
        return 1
    return value/abs(value)


def interpolate_points(start: Point, end: Point):
    diffx = end.x - start.x
    diffy = end.y - start.y

    if diffx == 0:
        dy = int(sign(diffy))
        return [ Point(start.x, y) for y in range(start.y, end.y + dy, dy) ]

    if diffy == 0:
        dx = int(sign(diffx))
        return [ Point(x, start.y) for x in range(start.x, end.x + dx, dx) ]

    if abs(diffx) == abs(diffy):
        dx = int(sign(diffx))
        dy = int(sign(diffy))

        return [ Point(x, y) for x, y in zip(range(start.x, end.x + dx, dx), range(start.y, end.y + dy, dy)) ]

    raise ValueError(f"line slope not supported ({diffx}:{diffy})")
