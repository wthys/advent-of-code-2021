#!/usr/bin/env python3

from common import read_input, Point, neejbers, color, intlist, combine, clean, debug
from graph import Edge, Graph

from collections import namedtuple, defaultdict
from itertools import pairwise, product


class CaveGraph(Graph):
    def shortest_path(self, start, end):
        Q = set(self.V)
        dist = defaultdict(lambda: float('inf'))
        prev = defaultdict(lambda: None)
        dist[start] = 0

        
        while len(Q) > 0:
            u = sorted(Q, key=lambda v: dist[v])[0]
            Q.remove(u)

            print(f"to check: {len(Q)}  ", end = "\r")

            for v, cost in self.G[u].items():
                if v in Q:
                    alt = dist[u] + cost
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u

            if u == end:
                break

        print(" "*30, end="\r")

        path = []
        u = end
        while u:
            path.insert(0, u)
            u = prev[u]

        return path


    def shortest_path_astar(self, start, end):

        def hfunc(node):
            return abs(node.x - end.x) + abs(node.y - end.y)

        Q = set([start])
        prev = dict()
        
        g = defaultdict(lambda: float('inf'))
        g[start] = 0

        f = defaultdict(lambda: float('inf'))
        f[start] = hfunc(start)

        def construct_path(node):
            path = []
            while node in prev:
                path.insert(0, node)
                node = prev[node]
            path.insert(0, node)
            return path

        while len(Q) > 0:
            u = sorted(Q, key=lambda n: f[n])[0]
            
            if u == end:
                print(" "*30, end="\r")
                return construct_path(u)

            print(f"h({u.x: 4d}, {u.y: 4d}) = {hfunc(u): 4d}   ", end = "\r")

            Q.remove(u)
            for v, cost in self.G[u].items():
                alt = g[u] + cost
                if alt < g[v]:
                    prev[v] = u
                    g[v] = alt
                    f[v] = alt + hfunc(v)
                    if v not in Q:
                        Q.add(v)

        return None


    def path_cost(self, path):
        costs = [ self.G[s][e] for s, e in pairwise(path) ]
        return sum( costs )




def graph_from_grid(grid):
    dims = Point(len(grid[0]), len(grid))
    
    edges = []
    for i, j in product(range(dims.x), range(dims.y)):
        p = Point(i, j)
        for ni, nj in neejbers(i, j, diagonal=False):
            n = Point(ni, nj)
            try:
                edges.append(Edge(p, n, grid[n.y][n.x]))
            except IndexError:
                pass

    return CaveGraph(edges)


def pretty_grid_path(grid, path):
    if not debug():
        return

    print("+" + "-" * len(grid[0]) + "+")
    for j, row in enumerate(grid):
        line = ""
        for i, value in enumerate(row):
            if Point(i, j) in path:
                line += f"{color.BOLD + color.GREEN}{value}{color.END}"
            else:
                line += f"{color.FAINT}{value}{color.END}"
        print(f"|{line}|")
    print("+" + "-" * len(grid[0]) + "+")

        


def part_one(content):
    graph = graph_from_grid(content)

    start = Point(0, 0)
    end = Point(len(content[0]) - 1, len(content) - 1)

    path = graph.shortest_path_astar(start, end)
    
    pretty_grid_path(content, path)

    cost = graph.path_cost(path)
    return cost


def part_two(content):

    dims = Point(len(content[0]), len(content))

    # expand grid
    grid = [ list( int() for _ in range(dims.x * 5) ) for _ in
            range(dims.y * 5) ]

    def dist(s, e):
        return abs(e.x - s.x) + abs(e.y - s.y)

    def risk_wrap(risk):
        nrisk = risk % 9
        if nrisk == 0:
            return 9
        return nrisk

    for X, Y in product(range(5), range(5)):
        for y, row in enumerate(content):
            for x, risk in enumerate(row):
                i = dims.x * X + x
                j = dims.y * Y + y
                grid[j][i] = risk_wrap(risk + dist(Point(0,0), Point(X, Y)))


    graph = graph_from_grid(grid)

    start = Point(0, 0)
    end = Point(dims.x * 5 - 1, dims.y * 5 - 1)

    path = graph.shortest_path_astar(start, end)

    pretty_grid_path(grid, path)

    cost = graph.path_cost(path)
    return cost


if __name__ == "__main__":
    content = read_input(combine(intlist, clean))

    print(f"part 1: {part_one(content)}")
    print(f"part 2: {part_two(content)}")

