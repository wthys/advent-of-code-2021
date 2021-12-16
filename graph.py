import math

from dataclasses import dataclass
from collections import defaultdict, Counter
from typing import Any


@dataclass(frozen=True)
class Edge:
    start: Any
    end: Any
    cost: int = 1

    def reverse(self):
        return Edge(self.end, self.start, self.cost)


class Graph:
    def __init__(self, edges):
        self.G = defaultdict(lambda:defaultdict(lambda:math.inf))
        self.V = set()

        if edges is not None:
            for edge in edges:
                self.V.add(edge.start)
                self.V.add(edge.end)

                self.G[edge.start][edge.end] = edge.cost

    def neejbers(self, node):
        if node not in self.G:
            return set()
        return set(self.G[node])

    def paths_between(self, start, dest):
        visited = Counter()
        path = []

        return list(self.paths_between_util(start, dest, visited, path))

    def paths_between_util(self, node, dest, visited, path):
        visited[node] += 1
        path.append(node)
        if node == dest:
            yield list(path)
        else:
            for neejber in (self.neejbers(node) - set(visited.elements())):
                yield from self.paths_between_util(neejber, dest, visited, path)

        path.pop()
        visited[node] -= 1
