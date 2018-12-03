
import collections
import itertools
import re


Patch = collections.namedtuple('Patch', 'id,x,y,w,h')


def read(filepath):
    patches = []
    with open(filepath) as f:
        for line in f:
            m = re.search(r'(?i)(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)', line)
            if not m:
                print('"%s" does not match parse pattern' % (line, ))
            gd = m.groupdict()
            gd = {k: int(v) for k, v in gd.items()}
            p = Patch(**gd)
            patches.append(p)
    print('Got %s inputs' % (len(patches), ))
    return patches


def has_overlap(p0, p1):
    p0_x1_x = p0.x + p0.w
    p0_x1_y = p0.y + p0.h
    p1_x1_x = p1.x + p1.w
    p1_x1_y = p1.y + p1.h

    if p1_x1_x < p0.x or p0_x1_x < p1.x or p1_x1_y < p0.y or p0_x1_y < p1.y:
        return False

    return True


def solve(patches):
    overlap_count = {p: 0 for p in patches}
    for p0, p1 in itertools.combinations(patches, 2):
        if has_overlap(p0, p1) or has_overlap(p1, p0):
            # print('patches %s %s overlap' % (p0, p1))
            overlap_count[p0] += 1
            overlap_count[p1] += 1
    # print({p: c for p, c in overlap_count.items() if c == 0})
    if len({p: c for p, c in overlap_count.items() if c == 0}) > 1:
        print('Multiple solutions!')
        return None
    for p, count in overlap_count.items():
        if count == 0:
            # print(p.id)
            return p.id


def main():
    patches = read('pb00_input00.txt')
    _id = solve(patches)
    print(_id)

    patches = read('pb01_input01.txt')
    _id = solve(patches)
    print(_id)


__name__ == '__main__' and main()

