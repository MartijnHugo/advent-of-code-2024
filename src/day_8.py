from collections import defaultdict
from functools import reduce
from itertools import combinations
from math import gcd
from numpy import array, ndarray

antennas: dict[str, list[ndarray]] = defaultdict(list)

with open("src/day_8.txt", "r") as f:
    for i, l in enumerate(f.readlines()):
        height = i + 1
        for j, c in enumerate(l.rstrip()):
            width = j + 1
            if c.isalnum():
                antennas[c].append(array((i, j)))

TOP_LEFT = array((0, 0))
BOTTOM_RIGHT = array((height, width))

print(f"{height} x {width}")
print(antennas)
antinodes = []
harmonic_antinodes = []
for frequency in antennas:
    this_frequency_antennas = antennas[frequency]
    for first, second in combinations(this_frequency_antennas, 2):
        print(f"{first} - {second}")
        distance = second - first
        if distance[0] % 3 == 0 and distance[1] % 3 == 0:
            antinodes.append(tuple(first + distance / 3))
            antinodes.append(tuple(second - distance / 3))
        if all(first - distance >= TOP_LEFT) and all(first - distance < BOTTOM_RIGHT):
            antinodes.append(tuple(first - distance))
        if all(second + distance >= TOP_LEFT) and all(second + distance < BOTTOM_RIGHT):
            antinodes.append(tuple(second + distance))

        gcd_distance = distance / reduce(gcd, distance)

        factor = 0
        while all(first + factor*gcd_distance >= TOP_LEFT) and all(first + factor*gcd_distance < BOTTOM_RIGHT):
            harmonic_antinodes.append(tuple(first + factor*gcd_distance))
            factor += 1

        factor = 0
        while all(second - factor*gcd_distance >= TOP_LEFT) and all(second - factor*gcd_distance < BOTTOM_RIGHT):
            harmonic_antinodes.append(tuple(second - factor*gcd_distance))
            factor += 1

print(len(set(antinodes)))
print(len(set(harmonic_antinodes)))