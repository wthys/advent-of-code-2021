#/usr/bin/env python3


from common import read_input, clean, Area, neejbers, debug, color

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Image:
    data: defaultdict[str]
    n: int = 0

    def __getitem__(self, pos):
        return self.data[pos]

    def area(self):
        xs, ys = zip(*list(self.data))
        return Area(
                range(min(xs) - 1, max(xs) + 2),
                range(min(ys) - 1, max(ys) + 2)
                )

    def lit(self):
        return sum( 1 for c in self.data.values() if c == '#' )


class Enhancer:
    def __init__(self, algo):
        self._algo = algo
        self._switch = algo[0] == '#'
        self._trans = { '.' : '0', '#' : '1' }

    def __call__(self, image):
        if self._switch:
            dflt = [
                    self._algo[0],
                    self._algo[-1]
                    ][image.n % 2]
        else:
            dflt = '.'
        data = defaultdict(lambda:dflt)
        area = image.area()
        
        for y in area.y:
            for x in area.x:
                binary = "".join( self._trans[image[pos]] for pos in neejbers(x, y, center = True))
                idx = int(binary, 2)

                data[(x, y)] = self._algo[idx]


        return Image(data, image.n + 1)


def parse_input(content):
    algo = ""
    data = defaultdict(lambda:'.')

    done = False

    j = 0

    for line in content:
        if not done:
            if len(line):
                algo += line
            else:
                done = True
        else:
            for i, c in enumerate(line):
                data[(i, j)] = c
            j += 1

    return Enhancer(algo), Image(data)


def main():
    content = read_input(clean)

    print(f"part 1: {part_one(content)}")
    print(f"part 2: {part_two(content)}")


def print_image(image, last_line=None):
    if not debug():
        return

    area = image.area()

    if last_line is None:
        last_line = len(area.y)

    topbot = "+" + "-" * len(area.x[1:-1]) + "+"

    print(topbot)
    n = 0
    for y in area.y[1:-1]:
        if n < last_line:
            row = "".join( image[(x, y)] for x in area.x[1:-1] )
            print(f"|{row}|")
        else:
            break
        n += 1
    print(topbot)


def part_one(content):
    enhance, image = parse_input(content)

    debug(f"original:")
    print_image(image)

    image = enhance(image)
    debug(f"after first enhance:")
    print_image(image)

    image = enhance(image)
    debug(f"after second enhance:")
    print_image(image)

    return image.lit()


def part_two(content):
    enhance, image = parse_input(content)

    for i in range(50):
        image = enhance(image)
        debug(f"after enhance {i+1}")
        print_image(image, 5)

    print_image(image)

    return image.lit()


if __name__ == "__main__":
    main()
