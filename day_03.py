import functools
import re
from pathlib import Path

INPUTS = Path('inputs')

DAY = 3

f = INPUTS / f'day_{DAY:02d}.txt'

TREE = '#'

VELOCITIES = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]


def main():
    trees = set()

    w = 0
    h = 0

    for line in f.open().readlines():
        w = len(line)

        trees |= set((h, m.start()) for m in re.finditer(TREE, line))
        h += 1

    total_trees = []
    for v in VELOCITIES:
        x = y = 0
        found_trees = 0
        while True:
            is_tree = (x, y) in trees
            if is_tree:
                found_trees += 1

            x += v[0]
            y += v[1]

            y %= w  # Repeating to the right

            if x > h:
                break

        print(f'Found {found_trees} trees (out of {len(trees)})')
        total_trees.append(found_trees)

    print('Total Trees', total_trees, 'product = ', functools.reduce(lambda a, b: a * b, total_trees))


if __name__ == '__main__':
    main()
