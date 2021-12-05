#!/usr/bin/env python3

import fileinput


def ident(something):
    return something


def read_input(transform = None):
    if transform is None:
        transform = ident

    with fileinput.input() as content:
        return [ transform(line) for line in content ]


def sign(value):
    if value == 0:
        return 1
    return value/abs(value)
