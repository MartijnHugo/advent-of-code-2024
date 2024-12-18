from collections import defaultdict
from enum import Enum
import sys

sys.setrecursionlimit(4000)

class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

def get_turn_cost(d1: Direction, d2: Direction):
    if d1 == d2:
        return 0
    
    if (
        (d1 == Direction.NORTH and d2 in (Direction.EAST, Direction.WEST)) or 
        (d1 == Direction.EAST and d2 in (Direction.SOUTH, Direction.NORTH)) or
        (d1 == Direction.SOUTH and d2 in (Direction.WEST, Direction.EAST)) or 
        (d1 == Direction.WEST and d2 in (Direction.NORTH, Direction.SOUTH))   
    ):
        return 1000
    
    if (
        (d1 == Direction.NORTH and d2 == Direction.SOUTH) or 
        (d1 == Direction.EAST and d2 == Direction.WEST) or
        (d1 == Direction.SOUTH and d2 == Direction.NORTH) or 
        (d1 == Direction.WEST and d2 == Direction.EAST)   
    ):
        return 2000


obstacles: list[tuple[int, int]] = []

with open("day_16.txt", "r") as f:
    for i, l in enumerate(f.readlines()):
        for j, c in enumerate(l.rstrip()):
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
            elif c == "#":
                obstacles.append((i, j))

print(f"Start: {start}")
print(f"End: {end}")
print(f"Nr. of obstacles: {len(obstacles)}")

visited: dict[tuple[int, int], int] = defaultdict(lambda: 1_000_000)
costs: list[int] = [1_000_000]
tiles: dict[int, list[tuple[int, int]]] = defaultdict(list)

def explore(coord: tuple[int, int], cost: int, direction: Direction, path: list[tuple[int, int]]):
    global costs
    global visited
    global tiles
    # print(f"Old Coord: {coord}")

    if coord == end:
        visited[end] = min(cost, visited[end])
        print(f"Found the exit, cost: {cost}")
        costs.append(cost)
        tiles[cost] += path
    elif cost <= visited[coord] + 1000 and cost <= 130536:
        visited[coord] = cost
        
        for d in Direction:
            turn_cost = get_turn_cost(direction, d)
            if turn_cost == 2000:
                continue

            new_cost = cost + 1
            new_coord = coord[0] + d.value[0], coord[1] + d.value[1]
            # print(f"New Coord: {new_coord}")

            if new_coord in obstacles:
                continue

            if d != direction:
                new_cost += get_turn_cost(direction, d)

            explore(new_coord, new_cost, d, [*path, new_coord])

explore(start, 0, Direction.EAST, [start])

print(visited)
print(min(costs))
print(len(set(tiles[min(costs)])))
