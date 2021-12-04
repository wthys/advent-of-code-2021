#!/usr/bin/env python3

import fileinput

def read_input(transform = None):
    if transform is None:
        transform = lambda _, x: x

    with fileinput.input() as content:
        return [ transform(i, line) for i, line in enumerate(content) ]
