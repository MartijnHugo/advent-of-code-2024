from enum import StrEnum

class Op(StrEnum):
    adv = "0"
    bxl = "1"
    bst = "2"
    jnz = "3"
    bxc = "4"
    out = "5"
    bdv = "6"
    cdv = "7"

REGISTER = {
    "A": int(37222139739636),
    "B": 0,
    "C": 0
}
COMBO = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: "A",
    5: "B",
    6: "C",
}
PROGRAM = "".join([str(n) for n in [2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0]])
OUTPUT = ""
TRIED = []

def get_combo(operand: str) -> int:
    combo = COMBO[operand]
    if isinstance(combo, str):
        combo = REGISTER[combo]

    return combo

def execute(instruction_pointer: int = 0):
    if instruction_pointer >= len(PROGRAM):
        return
    
    global OUTPUT
    if not PROGRAM.startswith(OUTPUT):
        return

    op, operand = PROGRAM[instruction_pointer:instruction_pointer + 2]
    operand = int(operand)

    # print(f"INSTRUCTION: {instruction_pointer} - OP: {op} - OPERAND: {operand} - REGISTER: {REGISTER}")
    if op == Op.adv:
        combo = get_combo(operand)
        REGISTER["A"] = int(str(REGISTER["A"] / 2**combo).split(".")[0])
    elif op == Op.bxl:
        REGISTER["B"] = REGISTER["B"] ^ operand
    elif op == Op.bst:
        combo = get_combo(operand)
        REGISTER["B"] = combo % 8
    elif op == Op.jnz:
        if REGISTER["A"] != 0:
            instruction_pointer = operand - 2
    elif op == Op.bxc:
        REGISTER["B"] = REGISTER["B"] ^ REGISTER["C"]
    elif op == Op.out:
        combo = get_combo(operand)
        OUTPUT += str(combo % 8)
    elif op == Op.bdv:
        combo = get_combo(operand)
        REGISTER["B"] = int(str(REGISTER["A"] / 2**combo).split(".")[0])
    elif op == Op.cdv:
        combo = get_combo(operand)
        REGISTER["C"] = int(str(REGISTER["A"] / 2**combo).split(".")[0])
    else:
        raise

    execute(instruction_pointer + 2)

execute()
print(",".join(OUTPUT))

a = 44902825460
last = 0
increment = 2**36

while True:
    REGISTER["A"] = a
    REGISTER["B"] = 0
    REGISTER["C"] = 0
    OUTPUT = ""

    execute()

    if len(OUTPUT) > 13 and PROGRAM.startswith(OUTPUT[:-1]):
        print(f"{a} - {a-last}")
        last = a

    if OUTPUT == PROGRAM:
        print(a)
        break

    a += increment
