
import collections
import re


def solve(list_of_ids):
    count_twice = 0
    count_thrice = 0
    for _id in list_of_ids:
        print(_id)
        c = collections.Counter()
        for l in _id:
            c[l] += 1
        id_counts_twice = False
        id_counts_thrice = False
        for letter, count in c.items():
            if count == 2:
                print('"%s"=%s' % (letter, count))
                id_counts_twice = True
            elif count == 3:
                print('"%s"=%s' % (letter, count))
                id_counts_thrice = True
        if id_counts_twice:
            count_twice += 1
        if id_counts_thrice:
            count_thrice += 1
    print('count_twice= %s  count_thrice= %s' % (count_twice, count_thrice))
    return count_twice * count_thrice



def main():
    list_of_ids = [
        'abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab',
    ]
    checksum = solve(list_of_ids)
    print(checksum)

    with open('pb00_input.txt') as f:
        list_of_ids = [e.strip() for e in f.readlines() if e.strip()]
    checksum = solve(list_of_ids)
    print(checksum)


__name__ == '__main__' and main()

