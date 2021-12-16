#!/usr/bin/env python3

from common import read_input


HEX2BIN = {"0": "0000"}

class Transmission:
    def __init__(self, hexa):
        self._hex = hexa
        self._bits = "".join( f"{int(x,16):04b}" for x in hexa )


    @property
    def hex(self):
        return self._hex


    @property
    def bits(self):
        return self._bits


class Packet:
    def __init__(self, **kwds):
        self._version = kwds['version']
        self._type = kwds['type']
        super().__init__()

    @property
    def version(self):
        return self._version
    
    @property
    def type(self):
        return self._type

    def is_literal(self):
        return self.type == 4

    def is_operator(self):
        return not self.is_literal()


class LiteralPacket(Packet):
    def __init__(self, literal, **kwds):
        self._literal = literal
        super().__init__(**kwds)

    @property
    def literal(self):
        return self._literal

    def __str__(self):
        return f"LiteralPacket(v={self.version}, t={self.type}, lit={self.literal})"


class OperatorPacket(Packet):
    def __init__(self, mode, packets, **kwds):
        self._mode = mode
        self._packets = packets
        super().__init__(**kwds)

    @property
    def mode(self):
        return self._mode

    @property
    def packets(self):
        return self._packets[:]

    def __str__(self):
        pkts = ", ".join(str(p) for p in self.packets)
        return f"OperatorPacket(v={self.version}, t={self.type}, m={self.mode}, pkts=[{pkts}])"



def decode_packet(bits):

    version = int(bits[:3], 2)
    type_id = int(bits[3:6], 2)

    match type_id:
        case 4:
            literal = ""
            offset = 6
            while True:
                chunk = bits[offset: offset + 5]
                literal += chunk[1:]
                offset += 5

                if chunk[0] == "0":
                    break

            return LiteralPacket(int(literal, 2), version=version, type=type_id), bits[offset:]

            
        case t:
            mode = bits[6]
            subpackets = []
            offset = 7

            match mode:
                case "0":
                    sublen = int(bits[offset:offset + 15], 2)
                    offset += 15
                    subbits = bits[offset:offset + sublen]
                    offset += sublen

                    while len(subbits) > 0 and int(subbits, 2) > 0:
                        packet, subbits = decode_packet(subbits)
                        subpackets.append(packet)

                    return OperatorPacket(mode, subpackets, version=version, type=type_id), bits[offset:]

                case "1":
                    sublen = int(bits[offset:offset + 11], 2)
                    offset += 11
                    bits = bits[offset:]

                    while len(bits) > 0 and len(subpackets) < sublen:
                        packet, bits = decode_packet(bits)
                        subpackets.append(packet)
                    
                    return OperatorPacket(mode, subpackets, version=version, type=type_id), bits


def parse_transmission(source):
    return Transmission(source.strip())


def walk_packet(packet, func):
    if packet.is_operator():
        for p in packet.packets:
            walk_packet(p, func)
    func(packet)


class Accumulator:
    def __init__(self, initial):
        self._total = initial

    def accumulate(self, value):
        self._total += value

    def total(self):
        return self._total


def part_one(transmission):
    print(f"DEBUG: {transmission.hex} -> {transmission.bits}")

    packet, remainder = decode_packet(transmission.bits)
    print(f"  remainder: {remainder}")
    print(f"  packet: {packet}")

    total_version = Accumulator(0)

    def sum_version(packet):
        total_version.accumulate(packet.version)

    walk_packet(packet, sum_version)

    return total_version.total()


def part_two(transmission):
    return 'n/a'


def main():
    transmissions = read_input(parse_transmission)

    extra_info = len(transmissions) > 1

    for transmission in transmissions:
        if extra_info:
            print(f"part 1: {transmission.hex} -> {part_one(transmission)}")
        else:
            print(f"part 1: {part_one(transmission)}")

    for transmission in transmissions:
        if extra_info:
            print(f"part 2: {transmission.hex} -> {part_two(transmission)}")
        else:
            print(f"part 2: {part_two(transmission)}")


if __name__ == "__main__":
    main()