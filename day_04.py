import re
from pathlib import Path

INPUTS = Path('inputs')

DAY = 4

f = INPUTS / f'day_{DAY:02d}.txt'

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

OPTIONAL_FIELDS = set('cid')

EYE_COLOURS = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def main():

    with f.open() as f_o:
        passports = [p.replace('\n', ' ') for p in f_o.read().split('\n\n')]

    p_fields = [sorted(p.split(' ')) for p in passports]

    pass_ok = 0
    pass_val = 0

    for i, p in enumerate(p_fields):
        p_map = {field.split(':')[0]: field.split(':')[1] for field in p}

        p_set = set(p_map.keys())
        all_req = (p_set & REQUIRED_FIELDS == REQUIRED_FIELDS)

        if not all_req:
            print(i, 'missing', p_set & REQUIRED_FIELDS ^ REQUIRED_FIELDS)
            continue

        print(i, 'OK')
        pass_ok += 1
        if pass_valid(p_map):
            pass_val += 1

    print(f'# pass  OK: {pass_ok:3}')
    print(f'# pass VAL: {pass_val:3}')


def pass_valid(p):
    if not (1920 <= int(p['byr']) <= 2002):
        print_discarded(p, 'byr')
        return False

    if not (2010 <= int(p['iyr']) <= 2020):
        print_discarded(p, 'iyr')
        return False

    if not (2020 <= int(p['eyr']) <= 2030):
        print_discarded(p, 'eyr')
        return False

    if 'cm' in p['hgt']:
        if not (150 <= int(p['hgt'].replace('cm', '')) <= 193):
            print_discarded(p, 'hgt')
            return False
    elif 'in' in p['hgt']:
        if not (59 <= int(p['hgt'].replace('in', '')) <= 76):
            print_discarded(p, 'hgt')
            return False
    else:
        print_discarded(p, 'hgt')
        return False

    if not re.search('#[a-f0-9]{6}', p['hcl']):
        print_discarded(p, 'hcl')
        return False

    if p['ecl'] not in EYE_COLOURS:
        print_discarded(p, 'ecl')
        return False

    if len(p['pid']) != 9 or not p['pid'].isdecimal():
        print_discarded(p, 'pid')
        return False

    return True


def print_discarded(p, field):
    print('Discarded', field, p[field])


if __name__ == '__main__':
    main()
