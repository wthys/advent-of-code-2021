#!/usr/bin/env python3

import fileinput
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def ident(something):
    return something

def clean(something):
    return something.strip()

def intlist(something):
    return list(map(int, something))


def read_input(transform = None):
    if transform is None:
        transform = ident

    with fileinput.input() as content:
        return [ transform(line) for line in content ]


def sign(value):
    if value == 0:
        return 1
    return value/abs(value)


def neejbers(x, y, /, diagonal = None):
    if diagonal is None or diagonal:
        return [
                (x - 1, y - 1), (x + 0, y - 1), (x + 1, y - 1),
                (x - 1, y + 0),                 (x + 1, y + 0),
                (x - 1, y + 1), (x + 0, y + 1), (x + 1, y + 1)
                ]
    else:
        return [ (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1) ]


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

