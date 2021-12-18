#!/usr/bin/env python3


from common import read_input, combine, clean

import pyparsing as pp

def as_int(t):
    return int(t[0])

def as_pair(t):
    _, a, _, b, _ = t
    return (a, b)

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




def main():
    numbers = read_input(combine(parse_number, clean))

    for number in numbers:
        print(f"{number}")


if __name__ == "__main__":
    main()

