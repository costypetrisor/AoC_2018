
import collections
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


def solve(patches):
    land = collections.Counter()
    for p in patches:
        for x in range(p.x, p.x + p.w):
            for y in range(p.y, p.y + p.h):
                land[(x, y)] += 1
    overlap = 0
    for k, v in land.items():
        if v > 1:
            overlap += 1
    return overlap


def main():
    patches = read('pb00_input00.txt')
    overlap_surface = solve(patches)
    print(overlap_surface)

    patches = read('pb00_input01.txt')
    overlap_surface = solve(patches)
    print(overlap_surface)


__name__ == '__main__' and main()

