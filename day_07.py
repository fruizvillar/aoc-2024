import re
from pathlib import Path

INPUTS = Path('inputs')

DAY = 7

f = INPUTS / f'day_{DAY:02d}.txt'

bag_re = re.compile('([a-z ]+) bags contain (.* bags?)')

OUR_BAG = 'shiny gold'


def main():
    print(f'Day {DAY:02}')
    bags = {}
    with f.open() as f_o:
        bag_info = bag_re.findall(f_o.read())

    for b in bag_info:
        if 'no other bags' in b:
            dependencies = {}
        else:
            dependencies = {bx[2:].replace(' bags', '').replace(' bag', ''): int(bx[0]) for bx in b[1].split(', ')}
        bags[b[0]] = dependencies

    print(f'\nOur bag: "{OUR_BAG}" req: {bags[OUR_BAG]}')

    incr = -1
    usable_bags = {OUR_BAG}
    while incr:
        n_prev = len(usable_bags)
        for bag_c, possible_bags in bags.items():

            if bag_c == OUR_BAG or bag_c in usable_bags:
                continue

            for target_bag in possible_bags:
                if target_bag in usable_bags:
                    usable_bags.add(bag_c)
                    print(f'Added "{bag_c}" as it can be put into "{target_bag}"')

        print(len(usable_bags), usable_bags)
        n_post = len(usable_bags)
        incr = n_post - n_prev

    usable_bags.remove(OUR_BAG)
    print('Usable  bags:', len(usable_bags), usable_bags)
    print('Total bags:', len(bags))
    print()

    needed = {OUR_BAG: 1}
    total = 0

    while sum(needed.values()):
        print(needed)

        # Getting 1st val with dependencies
        n0 = [k for k, v in needed.items() if v][0]
        print(f'{n0} bags need {bags[n0]}')

        # Adding dependencies
        for _ in range(needed[n0]):  # we need N bags that need M and X bags, adding NxM and NxX
            for b, n in bags[n0].items():
                total += n
                if b in needed:
                    needed[b] += n
                else:
                    needed[b] = n

        needed[n0] = 0

    print('TOTAL NEEDED:', total)


if __name__ == '__main__':
    main()
