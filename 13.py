#!/usr/bin/env python3

import re

from common import read_input

from collections import namedtuple, Counter, defaultdict


Position = namedtuple('Position', ['x', 'y'])
Fold = namedtuple('Fold', ['direction', 'coordinate'])



class Sheet:
    def __init__(self, dots):
        self.contents = defaultdict(int)

        for dot in dots:
            self.contents[dot] += 1


    def bounds(self):
        xs = list(sorted( dot.x for dot in self.contents.keys() ))
        ys = list(sorted( dot.y for dot in self.contents.keys() ))

        return (Position( xs[0], ys[0]), Position(xs[-1], ys[-1]))

    def count_dots(self):
        return len([ n for n in self.contents.values() if n > 0 ])


    def foldY(self, y):

        bounds = self.bounds()

        bottom_size = bounds[1].y - y

        for j in range(bottom_size + 1):
            for i in range(bounds[0].x, bounds[1].x + 1):
                orig = Position(i, y + j)
                dest = Position(i, y - j)

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
                orig = Position(x + i, j)
                dest = Position(x - i, j)

                if i > 0:
                    n = self.contents[orig]
                    if n > 0:
                        self.contents[dest] += n

                if orig in self.contents:
                    del self.contents[orig]


    def __str__(self):
        bounds = self.bounds()

        topbot = "+" + "-" * (bounds[1].x - bounds[0].x + 1) + "+"

        sheet = [topbot]
        for j in range(bounds[0].y, bounds[1].y + 1):
            line = "|"
            for i in range(bounds[0].x, bounds[1].x + 1):
                n = self.contents[Position(i, j)]
                if n > 0:
                    line += '#'
                else:
                    line += ' '
            line += "|"
            sheet.append(line)
        sheet.append(topbot)

        return "\n".join(sheet)




def part_one(page):
    dots, instructions = page
    sheet = Sheet(dots)

    match instructions[0]:
        case Fold('x', x):
            sheet.foldX(x)
        case Fold('y', y):
            sheet.foldY(y)
        case _:
            pass

    return sheet.count_dots()


def part_two(page):
    dots, instructions = page
    sheet = Sheet(dots)

    for instr in instructions:
        match instr:
            case Fold('x', x):
                sheet.foldX(x)
            case Fold('y', y):
                sheet.foldY(y)
            case _:
                pass

    print(sheet)
    return '☝'


def parse_page():
    dots = []
    instructions = []
    
    all_dots = False

    def clean(x):
        return x.strip()

    for line in read_input(clean):
        if all_dots:
            m = re.match(r"fold along (?P<dir>[xy])=(?P<coord>[0-9]+)", line)
            if m:
                instructions.append(Fold(m.group('dir'), int(m.group('coord'))))
        else:
            m = re.match(r"([0-9]+),([0-9]+)", line)
            if m:
                dots.append(Position(int(m.group(1)), int(m.group(2))))
            else:
                all_dots = True

    return (dots, instructions)
                
    

def main():
    page = parse_page()

    #print(page)

    print(f"part1: {part_one(page)}")
    print(f"part2: {part_two(page)}")


if __name__ == "__main__":
    main()
