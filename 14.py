#!/usr/bin/env python3

import re

from common import read_input

from collections import namedtuple, Counter, defaultdict
from functools import cache
from itertools import pairwise


class Reactor:
    def __init__(self, reactions):
        self.reactions = { pair: element for pair, element in reactions }


    @cache
    def react(self, template, n = None):
        result = template[0]

        if n is None:
            n = 1

        for pair in pairwise(template):
            if pair in self.reactions:
                result += self.reactions[pair]
            result += pair[1]

        if n == 1:
            return result
        else:
            return self.react(result, n - 1)


def part_one(engine):
    template, reactions = engine

    reactor = Reactor(reactions)

    template = reactor.react(template, 10)

    ctr = Counter(template)
    most = ctr.most_common(1)[0]
    least = ctr.most_common()[-1]

    return most[1] - least[1]


def part_two(engine):
    return 'n/a'


def parse_input():
    template = ""
    reactions = []
    
    def clean(x):
        return x.strip()

    for i, line in enumerate(read_input(clean)):
        if i == 0:
            template = line
        else:
            m = re.match(r"(..)\s*->\s*(.)", line)
            if m:
                reactions.append(( tuple(m.group(1)), m.group(2) ))
                

    return (template, reactions)
                
    

def main():
    engine = parse_input()

    print(f"part1: {part_one(engine)}")
    print(f"part2: {part_two(engine)}")


if __name__ == "__main__":
    main()
