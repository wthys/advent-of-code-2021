#!/usr/bin/env python3

import re

from common import read_input, clean, debug

from collections import Counter
from itertools import pairwise

from time import time


def ensure_strictly_positive(n):
    if n is None:
        return 1
    else:
        if n <= 0:
            raise ValueError("n must be larger than 0")
        if int(n) != n:
            raise ValueError("n must be integer")

        return n


class Reactor:
    def __init__(self, reactions):
        self.reactions = { pair: element for pair, element in reactions }


    def __react(self, a, b):
        if (a, b) not in self.reactions:
            return None

        return self.reactions[(a, b)]


    def react(self, template, n = None):
        n = ensure_strictly_positive(n)

        result = template[0]

        for a, b in pairwise(template):
            newel = self.__react(a, b)
            if newel:
                result += newel
            result += b

        if n <= 1:
            return result
        else:
            return self.react(result, n - 1)


    def react2(self, template, n = None):
        n = ensure_strictly_positive(n)

        result = Counter()
        doubles = []

        for pair in pairwise(template):
            tmpl = self.react(pair, n)

            result.update(tmpl)
            doubles.append(tmpl[-1])

        result.subtract(doubles[:-1])

        return result


    def react3(self, template, n = None):
        n = ensure_strictly_positive(n)

        yield from self.__react3(template, n)
        yield template[-1]
    

    def __react3(self, template, n = None):
        for pair in pairwise(template):
            a, b = pair

            newel = self.__react(a, b)
            if newel:
                if n == 1:
                    yield a
                    yield newel
                else:
                    yield from self.__react3((a, newel, b), n - 1)


    def react4(self, template, n = None):
        n = ensure_strictly_positive(n)

        pairs = Counter(pairwise(template))
        elems = Counter(template)

        for i in range(n):
            new_pairs = Counter()
            for (a, b), count in pairs.items():
                newel = self.__react(a, b)

                if newel:
                    elems[newel] += count

                    new_pairs[(a, newel)] += count
                    new_pairs[(newel, b)] += count
                else:
                    new_pairs[(a, b)] += count

            pairs = new_pairs

        return elems





def part_one(engine):
    template, reactions = engine

    reactor = Reactor(reactions)

    ctr = reactor.react4(template, 10)
    debug(ctr)

    most = ctr.most_common(1)[0]
    least = ctr.most_common()[-1]

    return most[1] - least[1]


def part_two(engine):
    template, reactions = engine

    reactor = Reactor(reactions)

    ctr = reactor.react4(template, 40)
    debug(ctr)

    most = ctr.most_common(1)[0]
    least = ctr.most_common()[-1]

    return most[1] - least[1]


def parse_input(source = None):
    template = ""
    reactions = []

    if source is None:
        contents = read_input(clean)
    else:
        contents = source

    for i, line in enumerate(contents):
        if i == 0:
            template = line
        else:
            m = re.match(r"(..)\s*->\s*(.)", line)
            if m:
                reactions.append(( tuple(m.group(1)), m.group(2) ))
                

    return (template, reactions)
                
    

def main():
    engine = parse_input()

    print(f"part 1: {part_one(engine)}")
    print(f"part 2: {part_two(engine)}")


if __name__ == "__main__":
    main()
