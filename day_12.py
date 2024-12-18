from collections import defaultdict

garden: list[list[str]] = []

with open("day_12.txt", "r") as f:
    for l in f.readlines():
        garden.append([c for c in l.rstrip()])

width = len(garden[0])
height = len(garden)

print(garden)

islands: dict[str, tuple[int, int]] = {}
checked: list[tuple[int, int]] = []


def flood_recursive(matrix, start_row: int, start_col: int):
    width = len(matrix)
    height = len(matrix[0])

    plants = defaultdict(int)
    fences = defaultdict(int)

    def fill(row, col, start_plant):
        if matrix[row][col] != start_plant:
            fences[(start_row, start_col)] += 1
            return
        elif (row, col) in checked:
            return
        else:
            checked.append((row, col))

        plants[(start_row, start_col)] += 1
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n in neighbors:
            if 0 <= n[0] <= width - 1 and 0 <= n[1] <= height - 1:
                fill(n[0], n[1], start_plant)
            else:
                fences[(start_row, start_col)] += 1

    start_plant = matrix[start_row][start_col]
    fill(start_row, start_col, start_plant)
    return plants[(start_row, start_col)], fences[(start_row, start_col)]


total_price = 0

for i, row in enumerate(garden):
    for j, plant in enumerate(row):
        plants, fences = flood_recursive(garden, i, j)
        total_price += plants * fences

print(total_price)