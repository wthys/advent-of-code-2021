#!/usr/bin/env python3

from common import read_input, Point, combine, clean
from graph import Edge, Graph


class GraphOne(Graph):
    def paths_between_util(self, node, dest, visited, path):
        visited[node] += 1
        path.append(node)

        def meaningful_visits():
            mv = set()
            for u, visits in visited.items():
                if u.lower() == u and visits > 0:
                    mv.add(u)
            return mv

        if node == dest:
            yield list(path)
        else:
            for neejber in (self.neejbers(node) - meaningful_visits()):
                yield from self.paths_between_util(neejber, dest, visited, path)

        path.pop()
        visited[node] -= 1


class GraphTwo(Graph):
    def paths_between_util(self, node, dest, visited, path):
        visited[node] += 1
        if len([ k for k, v in visited.items() if k.lower() == k and v == 2 ]) <= 1:
            path.append(node)


            def meaningful_visits():
                mv = set()
                for u, visits in visited.items():
                    if u in ('start', 'end') and visits > 0:
                        mv.add(u)
                    elif u.lower() == u and visits > 1:
                        mv.add(u)
                return mv

            if node == dest:
                yield list(path)
            else:
                for neejber in (self.neejbers(node) - meaningful_visits()):
                    yield from self.paths_between_util(neejber, dest, visited, path)

            path.pop()
        visited[node] -= 1


def part_one(edges):
    caves = GraphOne(edges)

    paths = caves.paths_between('start', 'end')

    return len(paths)


def part_two(edges):
    caves = GraphTwo(edges)

    paths = caves.paths_between('start', 'end')

    return len(paths)


def parse_edge(line):
    start, end = line.split('-')
    return Edge(start, end)
    

def main():
    edges = read_input(combine(parse_edge, clean))

    # add in reverse edges
    edges += [ edge.reverse() for edge in edges ]

    print(f"part1: {part_one(edges)}")
    print(f"part2: {part_two(edges)}")


if __name__ == "__main__":
    main()
