#!/usr/bin/env python3

import sys


def read_input(filename):
    with open(filename) as content:
        return [int(line) for line in content]


def differences(measurements):
    diffs = []
    for i, depth in enumerate(measurements):
        if i > 0:
            diffs.append(depth - measurements[i - 1])
    return diffs

def n_measurement(measurements, n=1):
    if n < 1:
        raise ValueError("n must be at least 1")
    if int(n) != n:
        raise ValueError("n must be int")
    if n >= len(measurements):
        return measurements

    return [measurements[i:i+n] for i in range(len(measurements[:-n+1]))]


def diff_n(measurements, n=1):
    diffs = []
    slices = [sum(grp) for grp in n_measurement(measurements, n)]
    for i, total in enumerate(slices):
        if i > 0:
            diffs.append(total-slices[i-1])
    return diffs


def count_increases(measurements):
    return len([x for x in measurements if x > 0])


def main(filename):
    measurements = read_input(filename)
    print(f"part1: {count_increases(differences(measurements))}")
    print(f"part2: {count_increases(diff_n(measurements, 3))}")


if __name__ == "__main__":
    main(sys.argv[1])
