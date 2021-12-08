#!/usr/bin/env python3

from itertools import chain
from typing import NamedTuple,List
from collections import Counter

from common import read_input

"""
 aa
b  c
b  c
 dd
e  f
e  f
 gg


  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
--+---+---+---+---+---+---+---+---+---+---+--
a | x |   | x | x |   | x | x | x | x | x | 8
b | x |   |   |   | x | x | x |   | x | x | 6
c | x | x | x | x | x |   |   | x | x | x | 8
d |   |   | x | x | x | x | x |   | x | x | 7
e | x |   | x |   |   |   | x |   | x |   | 4
f | x | x |   | x | x | x | x | x | x | x | 9
g | x |   | x | x |   | x | x |   | x | x | 7
--+---+---+---+---+---+---+---+---+---+---+--
  | 6 | 2 | 5 | 5 | 4 | 5 | 6 | 3 | 7 | 6 |
"""


class Reading(NamedTuple):
    digits: List[str]
    reading: List[str]

    def map1478(self):
        one = set([ x for x in self.digits if len(x) == 2 ][0])
        four = set([ x for x in self.digits if len(x) == 4 ][0])
        seven = set([ x for x in self.digits if len(x) == 3 ][0])
        eight = set([ x for x in self.digits if len(x) == 7 ][0])

        return {"1": one, "4": four, "7": seven, "8": eight}

    def map_all(self):
        mapping = self.map1478()


        # only difference between 1 and 7
        segA = list((mapping["7"] - mapping["1"]))[0]


        # count frequency of use for each segment
        freq = Counter("".join(self.digits))

        # only segment with 9 uses
        segF = [k for k,v in freq.items() if v == 9][0]

        # only segment with 4 uses
        segE = [k for k,v in freq.items() if v == 4][0]

        # only segment with 6 uses
        segB = [k for k,v in freq.items() if v == 6][0]

        # only segment with 8 uses that is not the a-segment
        segC = [k for k,v in freq.items() if v == 8 and k != segA][0]


        # only digit that doesn't use the f-segment
        mapping["2"] = set([ x for x in self.digits if segF not in x][0])

        # only 5-segment digit that has the b-segment
        mapping["5"] = set([ x for x in self.digits if len(x) == 5 and segB in x][0])

        # only 5-segment digit that is not 2 or 5
        mapping["3"] = set([ x for x in self.digits if len(x) == 5 and set(x) != mapping["2"] and set(x) != mapping["5"]][0])

        # only common segment between 2, 3, 4 and 5
        segD = list(mapping["2"] & mapping["3"] & mapping["4"] & mapping["5"])[0]

        mapping["0"] = set([ x for x in self.digits if len(x) == 6 and segD not in x][0])
        mapping["6"] = set([ x for x in self.digits if len(x) == 6 and segC not in x][0])
        mapping["9"] = set([ x for x in self.digits if len(x) == 6 and segE not in x][0])

        if len(mapping) != 10:
            missing = set(range(10)) - set(mapping.keys())
            raise ValueError(f"expected 10 values, got {len(mapping)}, missing: {missing}")

        return mapping


    def translate1478(self):
        #print(f"digits: {self.digits}, reading: {self.reading}")

        trans = ""
        mapping = self.map1478()
        for digit in self.reading:
            dig = set(digit)
            char = "."
            for candidate, segments in mapping.items():
                if dig == segments:
                    char = candidate
                    break
            trans += char
        
        return trans

    def translate(self):
        mapping = self.map_all()

        trans = ""
        for digit in self.reading:
            dig = set(digit)
            char = "."
            for candidate, segments in mapping.items():
                if dig == segments:
                    char = candidate
                    break
            trans += char

        return trans


def parse_reading(source):
    digits, reading = [x.strip() for x in source.split('|')]

    return Reading(digits = digits.strip().split(' '), reading = reading.strip().split(' '))


def part_one(readings):
    translations = [ reading.translate1478() for reading in readings ]

    counter = Counter("".join(translations))

    return counter["1"] + counter["4"] + counter["7"] + counter["8"]


def part_two(readings):
    translations = [ reading.translate() for reading in readings ]
    
    return sum( int(trans) for trans in translations )
    

def main():
    readings = read_input(parse_reading)

    print(f"part1: {part_one(readings)}")
    print(f"part2: {part_two(readings)}")


if __name__ == "__main__":
    main()
