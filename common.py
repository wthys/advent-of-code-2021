#!/usr/bin/env python3

import fileinput
import os

from collections import Counter
from dataclasses import dataclass
from typing import List


def debug(value=None):
    dbg = os.environ.get('DEBUG', "false")
    if dbg.lower() in ('false', 'no', 'f', 'n', '0', 'd', 'disabled'):
        return False
    if value:
        print(value)
    return True


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def subtract(self, other):
        match other:
            case Point(x, y):
                return Point(self.x - x, self.y - y)
            case (x, y):
                return Point(self.x - x, self.y - y)
            case _:
                raise ValueError(f"other is not a Point or tuple (got {type(other)})")

    def __sub__(self, other):
        return self.subtract(other)

    def add(self, other):
        match other:
            case Point(x, y):
                return Point(self.x + x, self.y + y)
            case (x, y):
                return Point(self.x + x, self.y + y)
            case _:
                raise ValueError(f"other is not a Point or tuple (got {type(other)})")

    def __add__(self, other):
        return self.add(other)




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
    FAINT = '\033[2m'
    END = '\033[0m'


def ident(something):
    return something

def clean(something):
    return something.strip()

def intlist(something):
    return list(map(int, something))

def combine(*funcs):
    def comb(something):
        for f in reversed(funcs):
            something = f(something)
        return something
    return comb


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


def interpolate_points(start, end):
    diff = end.subtract(start)

    if diff.x == 0:
        dy = int(sign(diff.y))
        return [ Point(start.x, y) for y in range(start.y, end.y + dy, dy) ]

    if diff.y == 0:
        dx = int(sign(diff.x))
        return [ Point(x, start.y) for x in range(start.x, end.x + dx, dx) ]

    if abs(diff.x) == abs(diff.y):
        dx = int(sign(diff.x))
        dy = int(sign(diff.y))

        return [ Point(x, y) for x, y in zip(range(start.x, end.x + dx, dx), range(start.y, end.y + dy, dy)) ]

    raise ValueError(f"line slope not supported ({diff.x}:{diff.y})")
