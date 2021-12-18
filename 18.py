#!/usr/bin/env python3


from common import read_input, combine, clean, debug, color

import pyparsing as pp

from collections import namedtuple, defaultdict
from copy import deepcopy
from itertools import permutations


def as_int(t):
    return int(t[0])

def as_pair(t):
    _, a, _, b, _ = t
    return pp.ParseResults.List([a, b])

NUMBER = pp.Word(pp.nums).set_parse_action(as_int)
OPEN = pp.Char('[')
CLOSE = pp.Char(']')
COMMA = pp.Char(',')

sfn = pp.Forward().setName('sfn')
single = NUMBER
pair = (OPEN 
        + sfn.set_results_name('left')
        + COMMA
        + sfn.set_results_name('right')
        + CLOSE
        ).set_parse_action(as_pair)
sfn << ( single | pair ).set_results_name('num')


def sfn_split(number, done = None):
    number = deepcopy(number)
    if done is None:
        done = [False]

    if done[0]:
        return number


    def descend(num):
        if done[0]:
            return num

        match num:
            case [a, b]:
                return [descend(a), descend(b)]
            case _:
                if num >= 10:
                    done[0] = True
                    return [num // 2, num - num // 2]
                return num

    number = descend(number)
    if done[0]:
        pass#debug(f"--   split: {number}")
    return number


def sfn_explode(number, done = None):
    number = deepcopy(number)

    if done is None:
        done = [False]

    if done[0]:
        return number

    def find_fuse(num, trace = None):
        if trace is None:
            trace = []

        match num:
            case [a, b]:
                if isinstance(a, int) and isinstance(b, int):
                    if len(trace) >= 4:
                        return trace
                    else:
                        return []

                trc = find_fuse(num[0], trace + [0])
                if len(trc) > 0:
                    return trc
                return find_fuse(num[1], trace + [1])
            case _:
                return []

    trace = find_fuse(number)
    if len(trace) == 0:
        return number

    done[0] = True

    def pair_at(trace):
        pair = number
        for idx in trace:
            pair = pair[idx]
        return pair

    left, right = pair_at(trace)
    parent = pair_at(trace[:-1])

    parent[trace[-1]] = 0

    def find_prev(trace):
        # find first parent with a left
        trc = trace[:]
        while trc.pop() == 0:
            if len(trc) == 0:
                return False
        trc.append(0)

        while True:
            pair = pair_at(trc)
            match pair:
                case [_, a]:
                    trc.append(1)
                case _:
                    return trc

    def find_next(trace):
        # find first parent with a right
        trc = trace[:]
        while trc.pop() == 1:
            if len(trc) == 0:
                return False
        trc.append(1)

        while True:
            pair = pair_at(trc)
            match pair:
                case [a, _]:
                    trc.append(0)
                case _:
                    return trc

    prv = find_prev(trace)
    if prv:
        #debug(f"found prev @ {prv}")
        pair = pair_at(prv[:-1])
        #debug(f"before change @ {prv}: {pair} // {number}")
        pair[prv[-1]] += left
        #debug(f"after change  @ {prv}: {pair} // {number}")

    nxt = find_next(trace)
    if nxt:
        #debug(f"found next @ {nxt}")
        pair = pair_at(nxt[:-1])
        #debug(f"before change @ {nxt}: {pair} // {number}")
        pair[nxt[-1]] += right
        #debug(f"after change  @ {nxt}: {pair} // {number}")

    #debug(f"-- explode: {number}")
    return number
        

def sfn_add(a, b):
    number = [deepcopy(a), deepcopy(b)]

    done = [True]
    while done[0]:
        done[0] = False
        number = sfn_explode(number, done)
        number = sfn_split(number, done)

    return number


def sfn_mag(number):
    match number:
        case [a, b]:
            return 3 * sfn_mag(a) + 2 * sfn_mag(b)
        case _:
            return number


def parse_number(line):
    return sfn.parseString(line)[0]



test_case = namedtuple('test_case', ['func', 'args', 'expected'])

def tests():

    fails = [0]

    def sfn_test(expected, actual, message):
        if expected == actual:
            return
        fails[0] += 1
        print(f"{message} should return {expected}, got {actual}")

    cases = [
            test_case(sfn_explode, ([[[[[9,8],1],2],3],4],), [[[[0,9],2],3],4] ),
            test_case(sfn_explode, ([7,[6,[5,[4,[3,2]]]]],), [7,[6,[5,[7,0]]]] ),
            test_case(sfn_explode, ([[6,[5,[4,[3,2]]]],1],), [[6,[5,[7,0]]],3] ),
            test_case(sfn_explode, ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],), [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]),
            test_case(sfn_explode, ([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],), [[3,[2,[8,0]]],[9,[5,[7,0]]]]),
            test_case(sfn_split, (10,), [5,5] ),
            test_case(sfn_split, (11,), [5,6] ),
            test_case(sfn_split, (18,), [9,9] ),
            test_case(sfn_add, ([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]), [[[[0,7],4],[[7,8],[6,0]]],[8,1]] ),
            test_case(sfn_mag, ([[1,2],[[3,4],5]],), 143),
            test_case(sfn_mag, ([[[[0,7],4],[[7,8],[6,0]]],[8,1]],), 1384),
            test_case(sfn_mag, ([[[[1,1],[2,2]],[3,3]],[4,4]],), 445),
            test_case(sfn_mag, ([[[[3,0],[5,3]],[4,4]],[5,5]],), 791),
            test_case(sfn_mag, ([[[[5,0],[7,4]],[5,5]],[6,6]],), 1137),
            test_case(sfn_mag, ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]],), 3488),
            ]

    for cs in cases:
        sfn_test(cs.expected, cs.func(*(cs.args)), f"{cs.func.__name__}({', '.join(map(str,cs.args))})")
    
    return fails[0]



def main():
    numbers = read_input(combine(parse_number, clean))

    if tests() > 0:
        return

    print(f"part 1: {part_one(numbers[:])}")
    print(f"part 2: {part_two(numbers[:])}")


def part_one(numbers):

    total = numbers[0]
    for number in numbers[1:]:
        debug(" ")
        debug(f"  {total}")
        debug(f"+ {number}")
        total = sfn_add(total, number)
        debug(f"= {total}")


    return sfn_mag(total)

def part_two(numbers):

    largest = (0, [])

    for a, b in permutations(numbers, 2):
        total = sfn_add(a, b)
        mag = sfn_mag(total)
        if mag > largest[0]:
            debug(" ")
            debug(f"{color.RED}{color.BOLD}NEW LARGEST @ {mag}{color.END}")
            debug(f"  {a}")
            debug(f"+ {b}")
            debug(f"= {total}")
            largest = (mag, total)


    return largest[0]


if __name__ == "__main__":
    main()

