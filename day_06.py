import functools
import re
from pathlib import Path

INPUTS = Path('inputs')

DAY = 6

f = INPUTS / f'day_{DAY:02d}.txt'


def main():

    with f.open() as f_o:
        groups = [p.replace('\n', ' ') for p in f_o.read().split('\n\n')]

    count_any = 0
    count_all = 0
    for i, g in enumerate(groups):

        n_answers_any = len(set(g.replace(' ', '')))
        print(f'{i}:, ANY: {n_answers_any}')

        answers = [set(x) for x in g.split(' ')]

        n_answers_all = len(functools.reduce(lambda a, b: a & b, answers))
        print(f'{i}:, ALL: {n_answers_all}')

        count_any += n_answers_any
        count_all += n_answers_all

    print()
    print('Count any', count_any)
    print('Count all', count_all)


if __name__ == '__main__':
    main()
