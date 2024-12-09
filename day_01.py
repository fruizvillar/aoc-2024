from pathlib import Path

INPUTS = Path('inputs')

DAY = 1

f = INPUTS / f'day_{DAY:02d}.txt'

GOAL = 2020
array = []

found1 = False
found2 = False

for line in f.open().readlines():

    n = int(line)

    for a1 in array:

        # Part 1
        if not found1:
            if a1 + n == GOAL:
                print(f'Found (part 1), {n} + {a1}')
                print(f'{n} * {a1}= {n * a1}')
                found1 = True

        # Part 2
        if not found2:
            for a2 in array:
                if a1 + a2 + n == GOAL:
                    print(f'Found (part 2), {n} + {a1} + {a2}')
                    print(f'{n} * {a1} * {a2} = {n * a1 * a2}')
                    found2 = True
                    break

        if found1 and found2:
            break
    else:
        array.append(n)

    if found1 and found2:
        break
