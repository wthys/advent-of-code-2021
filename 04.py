#!/usr/bin/env python3

from itertools import chain, compress

from common import read_input, clean


class BingoBoard:
    def __init__(self, numbers):
        if len(numbers) != 5:
            raise ValueError(f"Incorrect number of rows on bingo board (expected 5, got {len(numbers)})")
        
        self.grid = []
        for i, row in enumerate(numbers):
            if len(row) != 5:
                raise ValueError(f"Incorrect number of columns in row {i+1} (expected 5, got {len(row)})")
            
            self.grid.append(row[:])


    def has_bingo(self, drawn):
        dd = set(drawn)

        if len(dd) < 5:
            return False

        def is_filled(group):
            return len(set(group) - dd) == 0

        for i, row in enumerate(self.grid):
            if is_filled(row):
                #print(f"row {i+1} filled")
                return True

        for i, col in enumerate(zip(*self.grid)):
            if is_filled(col):
                #print(f"column {i+1} filled")
                return True

        return False


    def score(self, drawn):
        if not self.has_bingo(drawn):
            return -1
        
        return sum( set(chain(*self.grid)) - set(drawn) ) * drawn[-1]

    
    def __str__(self):
        board = "\n".join(" ".join(f"{x: 3d}" for x in row) for row in self.grid)
        return f"""-----BEGIN BOARD-----
{board}
-----END BOARD-----"""


def parse_input():
    content = read_input(clean)
    drawn = []
    boards = []
    board = None
    for i, line in enumerate(content):
        if i == 0:
            drawn = [ int(x) for x in line.strip().split(',') ]
        elif i % 6 == 1:
            if board is not None:
                boards.append(BingoBoard(board))
            board = []
        else:
            board.append([ int(x) for x in line.strip().split()])
    if board is not None:
        boards.append(BingoBoard(board))

    return drawn, boards


def part_one(drawn, boards):
    for n in range(len(drawn)):
        current_drawn = drawn[:n]
        for i, board in enumerate(boards):
            score = board.score(current_drawn)
            if score >= 0:
                #print(f"drawn: {current_drawn}, board: {i+1}")
                #print(board)
                return score


def part_two(drawn, boards):
    for n in range(len(drawn), 0, -1):
        current_drawn = drawn[:n]
        losing_boards = [ board for board in boards if board.score(current_drawn) < 0 ]
        if len(losing_boards) == 0:
            continue
        if len(losing_boards) == 1:
            return losing_boards[0].score(drawn[:n+1])
    
                

def main():
    drawn, boards = parse_input()

    #print(f"drawn: {drawn}")
    #print("boards:")
    #for board in boards:
    #    print(board)

    print(f"part 1: {part_one(drawn, boards)}")
    print(f"part 2: {part_two(drawn, boards)}")


if __name__ == "__main__":
    main()
