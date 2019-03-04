import json
from itertools import combinations

stats = {}
base = [i for i in range(0, 6)]

for i in range(1, 7):
    for x in combinations(base, i):
        stats[x] = 0

db = json.load(open('cleaned_db.json', 'r'))
for each in db:
    pairs = db[each]['QApairs']
    for pair in pairs:
        t = set(pair['type'])

        try:
            t.remove(6)
            t.add(3)
        except Exception as e:
            pass

        try:
            t.remove(7)
            t.add(4)
        except Exception as e:
            pass

        for i in range(1, len(t) + 1):
            for x in combinations(t, i):
                stats[x] += 1

stats = {k: v for k, v in stats.items() if v}
stats[(2,)] += 84
print(stats)

