import re

total = 0

lines = []
with open("src/day_3.txt", "r") as f:
    for l in f.readlines():
        lines.append(l)

def lekker_vermenigvuldigen(string) -> int:
    getal = 0
    multiplications = re.findall(r"mul\((?P<first>\d+)\,(?P<second>\d+)\)", string)
    for mul in multiplications:
        getal += int(mul[0]) * int(mul[1])

    return getal

for l in lines:
    total += lekker_vermenigvuldigen(l)


print(total)
total = 0

text = "".join(lines).replace("\n", "")
donts = text.split("don't()")
alldos = [donts[0]]
for dont in donts[1:]:
    dos = dont.split("do()") 
    if len(dos) > 1:
        alldos += dos[1:]

for do in alldos:
    total += lekker_vermenigvuldigen(do)

print(total)