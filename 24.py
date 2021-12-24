#!/usr/bin/env python3


from common import read_input, combine, clean, debug, color


from collections import namedtuple, defaultdict
from dataclasses import dataclass, field
from itertools import product


def register(reg, throw = None):
    if reg in "wxyz":
        return True
    if throw:
        raise ValueError(f"{reg} is not a valid register")
    return False


@dataclass
class Memory:
    input: list[int] = field(default_factory=list)
    registers: dict[str] = field(default_factory=lambda: defaultdict(int))

    def __getitem__(self, reg):
        register(reg, True)
        return self.registers[reg]

    def __setitem__(self, reg, value):
        register(reg, True)
        self.registers[reg] = value

    def read_input(self):
        return self.input.pop(0)

    def __str__(self):
        inp = ",".join(map(str, self.input))
        w,x,y,z = "wxyz"
        return f"Memory(w={self[w]}, x={self[x]}, y={self[y]}, z={self[z]}, inp=[{inp}])"


class ALU:
    def __init__(self, memory = None):
        if memory is None:
            memory = Memory(input=[])
        self.memory = memory

    def inp(self, a):
        register(a, True)
        self.memory[a] = self.memory.read_input()
        return self

    def add(self, a, b):
        register(a, True)
        if register(b):
            b = self.memory[b]
        self.memory[a] = self.memory[a] + int(b)
        return self

    def mul(self, a, b):
        register(a, True)
        if register(b):
            b = self.memory[b]
        self.memory[a] = self.memory[a] * int(b)
        return self

    def div(self, a, b):
        register(a, True)
        if register(b):
            b = self.memory[b]
        result = self.memory[a] // int(b)
        if result < 0:
            result += 1
        self.memory[a] = result
        return self

    def mod(self, a, b):
        register(a, True)
        if register(b):
            b = self.memory[b]
        aa = self.memory[a]
        bb = int(b)
        if aa < 0:
            raise ValueError(f"a must be 0 or larger, got {aa}")
        if bb <= 0:
            raise ValueError(f"b must be larger than 0, got {bb}")
        self.memory[a] = self.memory[a] % int(b)
        return self

    def eql(self, a, b):
        register(a, True)
        if register(b):
            b = self.memory[b]
        self.memory[a] = int(self.memory[a] == int(b))
        return self


def parse_instr(instr):
    parts = instr.split(' ')
    match parts:
        case ['inp', a]:
            def inp(alu):
                return alu.inp(a)
            inp.__doc__ = f"inp {a}"
            return inp
        
        case ['add', a, b]:
            def add(alu):
                return alu.add(a, b)
            add.__doc__ = f"add {a} {b}"
            return add
        
        case ['mul', a, b]:
            def mul(alu):
                return alu.mul(a, b)
            mul.__doc__ = f"mul {a} {b}"
            return mul
        
        case ['div', a, b]:
            def div(alu):
                return alu.div(a, b)
            div.__doc__ = f"div {a} {b}"
            return div
        
        case ['mod', a, b]:
            def mod(alu):
                return alu.mod(a, b)
            mod.__doc__ = f"mod {a} {b}"
            return mod

        case ['eql', a, b]:
            def eql(alu):
                return alu.eql(a, b)
            eql.__doc__ = f"eql {a} {b}"
            return eql

        case _:
            raise ValueError(f"Could not make sense of `{instr}`")


def main():
    instructions = read_input(combine(parse_instr, clean))

    def program(memory, verbose=None):
        alu = ALU(memory)
        for instr in instructions:
            if verbose:
                print(f"  executing: {instr.__doc__} => ", end = '')

            instr(alu)
            if verbose:
                print(f"{color.FAINT}{alu.memory}{color.END}")

    def is_serial(data):
        mem = Memory(input=list(data))
        try:
            program(mem, False)
            debug(f"  {''.join(map(str, data))} => {mem}")
            return mem['z'] == 0
        except Exception as e:
            debug(f"  {''.join(map(str, data))} => {mem} {color.BOLD}{color.RED}--> {e}{color.END} ||")
            return False

    digits = range(9, 0, -1)

    #for data in product([9], [9], digits):
    #    is_serial(data)

    d1 = [ n for n in digits if n + 5 in digits ]
    d2 = [ n for n in digits if n + 4 in digits ]
    d3 = [ n for n in digits if n - 8 in digits ]
    d4 = [ n for n in digits if n + 1 in digits ]
    d5 = [ (4,  1) ]
    d6 = [ n for n in digits if n - 7 in digits ]
    d7 = [ (6, -7) ]
    d8 = [ n for n in digits if n - 3 in digits ]
    d9 = [ n for n in digits if n - 5 in digits ]
    d10= [ (9, -5) ]
    d11= [ (8, -3) ]
    d12= [ (3, -8) ]
    d13= [ (2,  4) ]
    d14= [ (1,  5) ]


    serials = []

    for data in product(d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14):
        data = list(data)
        for idx, value in enumerate(data):
            match value:
                case (src, add):
                    data[idx] = data[src - 1] + add
                case _:
                    pass

        if is_serial(data):
            serials.append(data)

    debug(f"found {len(serials)} serial numbers")

    largest = ''.join(map(str, max(serials)))
    print(f"part 1: {largest}")
    smallest = ''.join(map(str, min(serials)))
    print(f"part 2: {smallest}")


if __name__ == "__main__":
    main()
