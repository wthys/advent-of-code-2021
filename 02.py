#!/usr/bin/env python3

import re

from collections import namedtuple

from common import read_input

Command = namedtuple('Command', ['command', 'distance'])
Position = namedtuple('Position', ['x', 'y', 'aim'])


def parse_command(cmd):
    m = re.match(r"(?P<command>forward|down|up)\s+(?P<distance>\d+)", cmd)

    if not m:
        return None

    return Command(m.group('command'), int(m.group('distance')))


def part1_cmddir():
    def forward(pos, n):
        return Position(pos.x + n, pos.y, 0)

    def up(pos, n):
        return Position(pos.x, pos.y - n, 0)

    def down(pos, n):
        return Position(pos.x, pos.y + n, 0)

    return { 'forward': forward, 'up': up, 'down': down }


def part2_cmddir():
    def forward(pos, n):
        return Position(pos.x + n, pos.y + pos.aim * n, pos.aim)

    def up(pos, n):
        return Position(pos.x, pos.y, pos.aim - n)

    def down(pos, n):
        return Position(pos.x, pos.y, pos.aim + n)

    return { 'forward': forward, 'up': up, 'down': down }


def travel(commands, cmd_dir):
    position = Position(0,0,0)
    
    for cmd in commands:
        if cmd is None:
            continue

        position = cmd_dir[cmd.command](position, cmd.distance)

    return position


def main():
    commands = read_input(parse_command)

    sol1 = travel(commands, part1_cmddir())
    print(f"part 1: {sol1.x * sol1.y}")

    sol2 = travel(commands, part2_cmddir())
    print(f"part 2: {sol2.x * sol2.y}")


if __name__ == "__main__":
    main()
