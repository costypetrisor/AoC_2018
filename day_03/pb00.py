
import collections
import datetime
import functools
import itertools
import json
import re



def read(filepath):
    records = []
    with open(filepath) as f:
        current_guard_id = None
        for line in f:
            line = line.strip()
            if not line:
                continue
        #     print(line)
            m = re.search(r'(?i)^\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)\s+(?P<hour>\d+):(?P<minute>\d+)\]\s+(?P<message>.*)', line)
            if not m:
                print('Unparsed: %s' % line)
            gd = m.groupdict()
            for e in ('year', 'month', 'day', 'hour', 'minute'):
                gd[e] = int(gd[e])
            date = (gd['year'], gd['month'], gd['day'], gd['hour'], gd['minute'])

            message = gd['message']
        #     print(date, message)
            m2 = re.search(r'(?i)Guard #(?P<_id>\d+) begins shift', message)
            if m2:
                current_guard_id = int(m2.group('_id'))
                records.append([date, current_guard_id, 'begins_shift'])
                continue
            m2 = re.search(r'(?i)falls asleep', message)
            if m2:
                records.append([date, None, 'falls_asleep'])
                continue
            m2 = re.search(r'(?i)wakes up', message)
            if m2:
                records.append([date, None, 'wakes_up'])
                continue
    return records



def solve(records):
    records = sorted(records, key=lambda r: (r[0]))
    current_guard_id = None
    for r in records:
        if r[2] == 'begins_shift':
            current_guard_id = r[1]
        else:
            r[1] = current_guard_id
    records = sorted(records, key=lambda r: (r[1], r[0]))
#     for r in records:
#         print(r)
    with open('intermediate.txt', 'w') as f:
        for r in records:
            f.write(str(r) + '\n')

    asleep_by_guard_id = collections.Counter()
    guard_states = {}
    for record in records:
        if record[2] == 'falls_asleep':
            guard_states[record[1]] = [record[0], ]
            continue
        elif record[2] == 'wakes_up':
            if record[1] in guard_states:
                asleep = guard_states[record[1]][0]
                if asleep[:3] != record[0][:3]:
                    print('Warning !!!! Guard #%s slept for multiple days' % (record[1], ))
                duration = datetime.datetime(*record[0]) - datetime.datetime(*asleep)
                asleep_minutes = int(duration.total_seconds() / 60)
                #     print('Guard #%s slept %s minutes' % (record[1], asleep_minutes))
                asleep_by_guard_id[record[1]] += asleep_minutes
            else:
                print('Error:   guard #%s wakes up but never been asleep' % (record[1], ))
    asleep_times_sorted = sorted(asleep_by_guard_id.items(), key=lambda x: x[1], reverse=True)
    print(asleep_times_sorted)
    guard_slept_the_most = asleep_times_sorted[0][0]
    print('Guard slept the most: %s' % (guard_slept_the_most, ))

    records_by_guard_id = collections.defaultdict(list)
    for r in records:
        records_by_guard_id[r[1]].append(r)

    our_guard_minutes_slept = collections.Counter()
    guard_states = {}
    for record in records_by_guard_id[guard_slept_the_most]:
        if record[2] == 'falls_asleep':
            guard_states[record[1]] = [record[0], ]
            continue
        elif record[2] == 'wakes_up':
            if record[1] in guard_states:
                asleep = guard_states[record[1]][0]
                if asleep[:3] != record[0][:3]:
                    print('Warning !!!! Guard #%s slept for multiple days' % (record[1], ))
                duration = datetime.datetime(*record[0]) - datetime.datetime(*asleep)
                asleep_minutes = int(duration.total_seconds() / 60)
                print('Guard #%s slept %s minutes from %s to %s' % (record[1], asleep_minutes, asleep[4], record[0][4]))
                for m in range(asleep[4], record[0][4]):
                    our_guard_minutes_slept[m] += 1
    minutes_slept = sorted(our_guard_minutes_slept.items(), key=lambda x: x[1], reverse=True)
    print(minutes_slept)
    most_slept_minute = minutes_slept[0][0]
    print(most_slept_minute)
    print(most_slept_minute * guard_slept_the_most)

    minutes_slept_guards = collections.defaultdict(collections.Counter)  # minutes -> guard_id -> times
    for guard_id in asleep_by_guard_id.keys():
        for record in records_by_guard_id[guard_id]:
            if record[2] == 'falls_asleep':
                guard_states[record[1]] = [record[0], ]
                continue
            elif record[2] == 'wakes_up':
                if record[1] in guard_states:
                    asleep = guard_states[record[1]][0]
                    if asleep[:3] != record[0][:3]:
                        print('Warning !!!! Guard #%s slept for multiple days' % (record[1], ))
                    duration = datetime.datetime(*record[0]) - datetime.datetime(*asleep)
                    asleep_minutes = int(duration.total_seconds() / 60)
                    # print('Guard #%s slept %s minutes from %s to %s' % (record[1], asleep_minutes, asleep[4], record[0][4]))
                    for m in range(asleep[4], record[0][4]):
                        minutes_slept_guards[m][guard_id] += 1
    # reverse minutes_slept_guards to minutes->times>guard_id
    minutes_slept_guards = {minutes: {times: guard_id for guard_id, times in v.items()} for minutes, v in minutes_slept_guards.items()}
    minutes_slept_guards = {minutes: sorted(v.items(), key=lambda e: e[0], reverse=True) for minutes, v in minutes_slept_guards.items()}
    minutes_slept_guards = sorted(minutes_slept_guards.items(), key=lambda e: e[1][0], reverse=True)
    # print(minutes_slept_guards)
    v = minutes_slept_guards[0]
    print(v)
    print('Answer 2: %s * %s    %s' % (v[0], v[1][0][1], v[0] * v[1][0][1], ) )

    return most_slept_minute * guard_slept_the_most



def main():
    input_00 = read('pb00_input00.txt')
    result_00 = solve(input_00)
    print(result_00)

    input_01 = read('pb00_input01.txt')
    result_01 = solve(input_01)
    print(result_01)


__name__ == '__main__' and main()
