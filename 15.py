#!/usr/bin/env python3

from common import read_input, Point, clean, neejbers

from collections import namedtuple, defaultdict
from itertools import pairwise


Edge = namedtuple('Edge', ['start', 'end', 'cost'])


class Graph:
    def __init__(self, edges):
        self.iE = defaultdict(lambda: defaultdict(lambda: float('inf')))
        self.oE = defaultdict(lambda: defaultdict(lambda: float('inf')))
        self.V = set()

        if edges is not None:
            for edge in edges:
                self.V.add(edge.start)
                self.V.add(edge.end)

                self.iE[edge.end][edge.start] = edge.cost 
                self.oE[edge.start][edge.end] = edge.cost

    def shortest_path(self, start, end):
        Q = set(self.V)
        dist = defaultdict(lambda: float('inf'))
        prev = defaultdict(lambda: None)
        dist[start] = 0

        while len(Q) > 0:
            u = sorted(Q, key=lambda v: dist[v])[0]
            Q.remove(u)

            for v, cost in self.oE[u].items():
                if v in Q:
                    alt = dist[u] + cost
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u

        path = []
        u = end
        while u:
            path.insert(0, u)
            u = prev[u]

        return path


    def path_cost(self, path):
        return sum( self.oE[s][e] for s, e in pairwise(path) )


def sane_neejbers(p, dims):
    nbh = [ Point(x, y) for x, y in neejbers(p.x, p.y, diagonal=False) ]
    return list(filter(lambda pt: pt.x in range(dims.x + 1) and pt.y in range(dims.y + 1), nbh))


def parse_content(content):
    grid = defaultdict(lambda: 10**100)

    dims = Point(len(content[0]), len(content))
    
    for j, row in enumerate(content):
        for i, value in enumerate(row):
            grid[Point(i, j)] = value

    edges = []
    
    for p in list(grid.keys()):
        for n in sane_neejbers(p, dims):
            edges.append(Edge(p, n, grid[n]))

    graph = Graph(edges)

    return grid, graph
        


def part_one(content):
    grid, graph = parse_content(content)

    start = Point(0, 0)
    end = Point(len(content[0]) - 1, len(content) - 1)

    path = graph.shortest_path(start, end)
    print(f"shortest path: {path}")

    cost = graph.path_cost(path)
    return cost


def part_two(content):
    return 'n/a'


if __name__ == "__main__":
    content = read_input(lambda line: list(map(int, line.strip())))

    print(f"part 1: {part_one(content)}")
    print(f"part 2: {part_two(content)}")

