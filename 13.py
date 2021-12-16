#!/usr/bin/env python3

import re

from common import read_input, Point, clean, debug, color

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Fold:
    direction: str
    coordinate: int


class Sheet:
    def __init__(self, dots):
        self.contents = defaultdict(int)

        for dot in dots:
            self.contents[dot] += 1

    def bounds(self):
        xs = list(sorted( dot.x for dot in self.contents.keys() ))
        ys = list(sorted( dot.y for dot in self.contents.keys() ))

        return (Point(xs[0], ys[0]), Point(xs[-1], ys[-1]))

    def count_dots(self):
        return len([ n for n in self.contents.values() if n > 0 ])

    def foldY(self, y):
        bounds = self.bounds()

        bottom_size = bounds[1].y - y

        for j in range(bottom_size + 1):
            for i in range(bounds[0].x, bounds[1].x + 1):
                orig = Point(i, y + j)
                dest = Point(i, y - j)

                if j > 0:
                    n = self.contents[orig]
                    if n > 0:
                        self.contents[dest] += n

                if orig in self.contents:
                    del self.contents[orig]

    def foldX(self, x):
        bounds = self.bounds()

        right_size = bounds[1].x - x

        for i in range(right_size + 1):
            for j in range(bounds[0].y, bounds[1].y + 1):
                orig = Point(x + i, j)
                dest = Point(x - i, j)

                if i > 0:
                    n = self.contents[orig]
                    if n > 0:
                        self.contents[dest] += n

                if orig in self.contents:
                    del self.contents[orig]

    def fold(self, instruction):
        match instruction:
            case Fold('x', x):
                self.foldX(x)
            case Fold('y', y):
                self.foldY(y)
            case _:
                pass

    def __str__(self):
        bounds = self.bounds()

        topbot = "+" + "-" * abs(bounds[1].x - bounds[0].x + 1) + "+"

        sheet = [topbot]
        for j in range(bounds[0].y, bounds[1].y + 1):
            line = "|"
            for i in range(bounds[0].x, bounds[1].x + 1):
                n = self.contents[Point(i, j)]
                if n > 0:
                    line += f"{color.BOLD}{color.GREEN}#{color.END}"
                else:
                    line += f"{color.FAINT}.{color.END}"
            line += "|"
            sheet.append(line)
        sheet.append(topbot)

        return "\n".join(sheet)


def part_one(page):
    dots, instructions = page
    sheet = Sheet(dots)

    debug("initial")
    debug(sheet)

    sheet.fold(instructions[0])
    
    debug(f"after {instructions[0]}")
    debug(sheet)

    return sheet.count_dots()


def part_two(page):
    dots, instructions = page
    sheet = Sheet(dots)

    debug("initial")
    debug(sheet)

    for instr in instructions:
        sheet.fold(instr)
        debug(f"after {instr}")
        debug(sheet)

    print(sheet)
    return '☝'


def parse_page():
    dots = []
    instructions = []
    
    all_dots = False

    for line in read_input(clean):
        if all_dots:
            m = re.match(r"fold along (?P<dir>[xy])=(?P<coord>[0-9]+)", line)
            if m:
                instructions.append(Fold(m.group('dir'), int(m.group('coord'))))
        else:
            m = re.match(r"([0-9]+),([0-9]+)", line)
            if m:
                dots.append(Point(int(m.group(1)), int(m.group(2))))
            else:
                all_dots = True

    return (dots, instructions)
    

def main():
    page = parse_page()

    print(f"part 1: {part_one(page)}")
    print(f"part 2: {part_two(page)}")


if __name__ == "__main__":
    main()
