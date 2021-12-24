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


@dataclass(frozen=False)
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

    print(f"part 1: {part_one(program)}")
    print(f"part 2: {part_two(program)}")
                

def part_one(program):

    for data in product([9,8,7,6,5,4,3,2,1], repeat=2):
        mem = Memory(input=list(data))
        try:
            program(mem)
        except ValueError as e:
            debug(f"  ==> {data} failed with {e}")
        except ZeroDivisionError as e:
            debug(f"  ==> {data} failed with {e}")
        else:
            debug(f"  ==> {data} resulted in {mem}")
    
    return 'n/a'


def part_two(program):
    return 'n/a'


if __name__ == "__main__":
    main()
