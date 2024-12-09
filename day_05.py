from pathlib import Path

INPUTS = Path('inputs')

DAY = 5

f = INPUTS / f'day_{DAY:02d}.txt'

BIN_VALUES = {'B': '1', 'F': '0', 'R': '1', 'L': '0'}


def main():

    with f.open() as f_o:
        seats = f_o.readlines()

    seat_ids = [binarize_set(s.strip()) for s in seats]

    for (i, s) in zip(seats, seat_ids):
        print(s, i)

    sid_min = min(seat_ids)
    sid_max = max(seat_ids)

    print('The highest seat ID is', sid_max)

    for n in range(sid_min, sid_max):
        if n not in seat_ids:
            print('Your seat is', n)


def binarize_set(s: str):
    for k, v in BIN_VALUES.items():
        s = s.replace(k, v)
    return int(s, 2)


def print_discarded(p, field):
    print('Discarded', field, p[field])


if __name__ == '__main__':
    main()
