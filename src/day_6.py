from copy import deepcopy
from dataclasses import asdict, dataclass, field
from enum import Enum
from tqdm import tqdm

class Space(Enum):
    EMPTY = "."
    OBSTACLE = "#"
    GUARD_UP = "^"
    GUARD_RIGHT = ">"
    GUARD_DOWN = "v"
    GUARD_LEFT = "<"

class Direction(Enum):
    UP = (-1, 0)
    UPRIGHT = (-1, 1)
    RIGHT = (0, 1)
    DOWNRIGHT = (1, 1)
    DOWN = (1, 0)
    DOWNLEFT = (1, -1)
    LEFT = (0, -1)
    UPLEFT = (-1, -1)


@dataclass
class Coord:
    row: int
    col: int

    def move(self, direction: Direction, steps: int = 1):
        self.row += direction.value[0] * steps
        self.col += direction.value[1] * steps

    def __eq__(self, other: "Coord"):
        return (self.row, self.col) == (other.row, other.col)

    def __hash__(self) -> int:
        return hash(f"{self.row}-{self.col}")


# @dataclass
# class Guard:
#     position: Coord
#     direction: Direction

#     def step(self):
#         self.position.move(self.direction)

#     def reverse(self):
#         self.position.move(self.direction, -1)

#     def turn(self):
#         if self.direction == Direction.UP:
#             self.direction = Direction.RIGHT
#         elif self.direction == Direction.RIGHT:
#             self.direction = Direction.DOWN
#         elif self.direction == Direction.DOWN:
#             self.direction = Direction.LEFT
#         elif self.direction == Direction.LEFT:
#             self.direction = Direction.UP
#         else:
#             raise

#     def __eq__(self, other: "Guard"):
#         return (self.position, self.direction) == (other.position, other.direction)

#     def __hash__(self) -> int:
#         return hash(f"{self.position.row}-{self.position.col}-{self.direction}")


# @dataclass
# class Grid:
#     guard: Guard
#     obstacles: list[Coord]
#     spaces: list[list[Space]]
#     timeline: list[Guard] = field(default_factory=list)
#     candidate_obstructions: list[Coord] = field(default_factory=list)

#     @property
#     def height(self) -> int:
#         return len(self.spaces)
    
#     @property
#     def width(self) -> int:
#         return len(self.spaces[0])

#     def exhaust_guard(self) -> bool:
#         while self.guard.position.row >= 0 and self.guard.position.row < self.height and self.guard.position.col >= 0 and self.guard.position.col < self.width:
#             if self.guard in self.timeline:
#                 return False
#             self.timeline.append(Guard(Coord(**asdict(self.guard.position)), self.guard.direction))
            

#             self.guard.step()
#             while self.guard.position in self.obstacles:
#                 self.guard.reverse()
#                 self.guard.turn()
#                 self.guard.step()

#         return True


# with open("src/day_6.txt", "r") as f:
#     obstacles: list[Coord] = []
#     spaces: list[list[Space]] = []
#     for i, l in enumerate(f.readlines()):
#         row: list[Space] = []
#         for j, c in enumerate(l.rstrip()):
#             if c == ".":
#                 row.append(Space.EMPTY)
#             elif c == "#":
#                 row.append(Space.OBSTACLE)
#                 obstacles.append(Coord(i, j))
#             elif c == "^":
#                 row.append(Space.GUARD_UP)
#                 guard = Guard(Coord(i, j), Direction.UP)
#             elif c == ">":
#                 row.append(Space.GUARD_RIGHT)
#                 guard = Guard(Coord(i, j), Direction.RIGHT)
#             elif c == "v":
#                 row.append(Space.GUARD_DOWN)
#                 guard = Guard(Coord(i, j), Direction.DOWN)
#             elif c == "<":
#                 row.append(Space.GUARD_LEFT)
#                 guard = Guard(Coord(i, j), Direction.LEFT)
#             else:
#                 raise

#         spaces.append(row)
    
#     initial_grid = Grid(guard, obstacles, spaces)

# a_grid = deepcopy(initial_grid)
# print(a_grid)
# exits = a_grid.exhaust_guard()
# print(len(set([g.position for g in a_grid.timeline])))

# timeline_coords = [g.position for g in a_grid.timeline]

# possible_obstructions = []
# for i in tqdm(range(initial_grid.height)):
#     for j in range(initial_grid.width):
#         if (candidate_obstruction := Coord(i, j)) not in timeline_coords:
#             continue

#         grid = deepcopy(initial_grid)
#         grid.obstacles.append(candidate_obstruction)
#         if not grid.exhaust_guard():
#             possible_obstructions.append(candidate_obstruction)


# print(possible_obstructions)