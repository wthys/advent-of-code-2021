#!/usr/bin/env python3

from collections import Counter

from common import read_input


def most_common(bits):
    mc = Counter(bits).most_common()

    if len(mc) == 1:
        return mc[0][0]

    most, least = mc

    if most[1] == least[1]:
        return "1"

    return most[0]


def gamma_epsilon(report, n=None):
    gamma = []
    epsilon = []

    epsmap = { "0" : "1", "1" : "0" }

    if n is None:
        n=len(report[0])
    if n < 1:
        raise ValueError("n must be at least 1")
    if int(n) != n:
        raise ValueError("n must be an int")
    
    #unzip the zipped list
    series = zip(*report)
    for i, bits in enumerate(series):
        if i >= n:
            break

        comm = most_common(bits)
        gamma.append(comm)
        epsilon.append(epsmap[comm])

    return "".join(gamma), "".join(epsilon)


def extract_rating(report, selector):
    if len(report) == 0:
        raise ValueError('no ratings available')

    if len(report) == 1:
        return report[0]
    
    gamma, epsilon = gamma_epsilon(report, 1)

    common_bit = selector(gamma, epsilon)[0]

    return common_bit + extract_rating( [x[1:] for x in report if x[0] == common_bit], selector )


def part_one(report):
    gamma, epsilon = gamma_epsilon(report)

    return int(gamma, 2) * int(epsilon, 2)


def part_two(report):
    oxy = int(extract_rating(report, lambda g, e: g), 2)
    co2 = int(extract_rating(report, lambda g, e: e), 2)

    return oxy * co2


def main():
    report = read_input(lambda x: x.strip())

    print(f"part1: {part_one(report)}")
    print(f"part2: {part_two(report)}")


if __name__ == "__main__":
    main()
