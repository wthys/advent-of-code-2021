#!/usr/bin/env python3


from common import read_input, combine, clean, debug

import pyparsing as pp

from collections import namedtuple


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



def parse_number(line):
    return sfn.parseString(line)[0]


def sfn_equals(a, b):
    if type(a) != type(b):
        return False

    match a:
        case [_, _]:
            return sfn_equals(a[0], b[0]) and sfn_equals(a[1], b[1])

        case _:
            return a == b


def sfn_split(number, done = None):
    if done is None:
        done = [False]

    def mark_done():
        done[0] = True

    if done[0]:
        return number

    match number:
        case [a, b]:
            return  [sfn_split(a, done), sfn_split(b, done)]
        case n:
            if n < 10:
                return n
            mark_done()
            return [n // 2, n - n // 2]


def should_explode(num, trace = None):
    if trace is None:
        trace = []

    match number:
        case [a, b]:
            if len(trace) >= 4:
                return False

            exa = should_explode(a, trace + [0])
            if exa:
                return exa

            return should_explode(b, trace + [1])
        case n:
            if len(trace) == 4:
                return trace
            return False


def sfn_explode(number, done = None):
    if done is None:
        done = [False]

    def mark_done():
        done[0] = True

    if done or len(number) == 1:
        return number

    trace = should_explode(number)
    if trace:
        mark_done()
        a, b, c, d = trace
        parent = number[a][b][c]
        pleft, pright = parent
        eleft, eright = parent[d]
        if d == 0:
            number[a][b][c] = [0, eright + pright]
        else:
            number[a][b][c] = [eleft + pleft, 0]
        return number

    a, b = number
    aa = sfn_explode(a)
    if not sfn_equals(a, aa):
        return [aa, b]

    return [a, sfn_explode(b)]


def sfn_reduce(number):
    debug(f"original:      {number}")
    while True:
        reduced = sfn_explode(number)
        debug(f"after explode: {reduced}")

        if sfn_equals(number, reduced):
            reduced = sfn_split(number)
            debug(f"after split:   {reduced}")

            if sfn_equals(number, reduced):
                return number

        number = reduced

def sfn_test(expected, actual, message):
    if sfn_equals(expected, actual):
        return
    print(f"{message} should return {expected}, got {actual}")


test_case = namedtuple('test_case', ['func', 'input', 'expected'])

def tests():
    cases = [
            test_case(sfn_explode, [[[[[9,8],1],2],3],4], [[[[0,9],2],3],4] ),
            test_case(sfn_explode, [7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]] ),
            test_case(sfn_explode, [[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3] ),
            test_case(sfn_explode, [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]),
            test_case(sfn_explode, [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[7,0]]]])
            test_case(sfn_split, 10, [5,5] ),
            test_case(sfn_split, 11, [5,6] ),
            test_case(sfn_split, 18, [9,9] ),
            ]

    for cs in cases:
        sfn_test(cs.expected, cs.func(cs.input), f"{cs.func.__name__}({cs.input})")


def main():
    numbers = read_input(combine(parse_number, clean))

    tests()

    print(sfn_reduce([[[[[4,3],4],4],[7,[[8,4],9]]], [1,1]]))

    


if __name__ == "__main__":
    main()

