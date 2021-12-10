#!/usr/bin/env python3

from common import read_input

from itertools import chain
from collections import namedtuple


EXPECTED = { "(" : ")", "{" : "}", "<" : ">", "[" : "]" }

NavSyntaxError = namedtuple('NavSyntaxError', ['idx', 'char'])

def find_error(line):
    context = []

    for i, char in enumerate(line):
        if char in EXPECTED:
            context.append(EXPECTED[char])
        elif char == context[-1]:
            context.pop()
        else:
            return NavSyntaxError(i, char)

    return None


def completion(line):
    context = []

    for i, char in enumerate(line):
        if char in EXPECTED:
            context.append(EXPECTED[char])
        else:
            expected = context[-1]
            if char == expected:
                context.pop()
            else:
                raise ValueError("could not complete line")

    return "".join(reversed(context))


def score_error(error):
    if error is None:
        return 0

    points = { ")" : 3, "]" : 57, "}" : 1197, ">" : 25137 }
    return points[error.char]


def score_completion(candidate):
    points = { ")" : 1, "]" : 2, "}" : 3, ">" : 4 }

    total = 0
    for char in candidate:
        total = total * 5 + points[char]

    return total


def part_one(source):
    errors = [ find_error(line) for line in source ]

    return sum(map(score_error, errors))


def part_two(source):
    completions = [ completion(line) for line in source if find_error(line) is None]

    scores = list(sorted(map(score_completion, completions)))

    return scores[len(scores)//2]


def clean(source):
    return source.strip()


def main():
    source = read_input(clean)
    print(f"part1: {part_one(source)}")
    print(f"part2: {part_two(source)}")


if __name__ == "__main__":
    main()
