#/usr/bin/env python3


from common import read_input, clean, Area, neejbers, debug, color

from collections import defaultdict


def parse_input(content):
    enhancer = ""
    image = defaultdict(lambda:'.')

    done = False

    j = 0

    for line in content:
        if not done:
            if len(line):
                enhancer += line
            else:
                done = True
        else:
            for i, c in enumerate(line):
                image[(i, j)] = c
            j += 1

    return enhancer, image


def enhance(image, algo):
    img = defaultdict(lambda:'.')
    area = area_from_image(image)

    trans = { '.' : '0', '#' : '1' }
    
    for y in area.y:
        for x in area.x:
            binary = "".join( trans[image[(i, j)]] for i, j in neejbers(x, y, center = True))
            idx = int(binary, 2)
            img[(x, y)] = algo[idx]

    return img



def area_from_image(image):
    xs, ys = zip(*list(image))
    return Area(
            range(min(xs) - 1, max(xs) + 2),
            range(min(ys) - 1, max(ys) + 2)
            )

def main():
    content = read_input(clean)

    print(f"part 1: {part_one(content)}")
    print(f"part 2: {part_two(content)}")


def print_image(image):
    if not debug():
        return

    area = area_from_image(image)

    topbot = "+" + "-" * len(area.x[1:-1]) + "+"

    print(topbot)
    for y in area.y[1:-1]:
        row = "".join( image[(x, y)] for x in area.x[1:-1] )
        print(f"|{row}|")
    print(topbot)


def part_one(content):
    algo, image = parse_input(content)

    debug(f"original:")
    print_image(image)

    image = enhance(image, algo)
    debug(f"after first enhance:")
    print_image(image)

    image = enhance(image, algo)
    debug(f"after second enhance:")
    print_image(image)

    return sum( 1 for c in image.values() if c == '#' )




def part_two(content):
    return 'n/a'


if __name__ == "__main__":
    main()
