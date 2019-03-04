import json
import random
from functools import reduce

db = json.load(open('cleaned_db.json', 'r'))

types = {'count': 0,
        'order': 1,
        'taste': 2,
        'when': 3,
        'reasoning': 4,
        'property': 5,
        'duration': 6,
        'freestyle': 7}

total = [{'num': 3980, 'ids': []},
         {'num': 3260, 'ids': []},
         {'num': 2000, 'ids': []},
         {'num': 3553, 'ids': []},
         {'num': 7200, 'ids': []},
         {'num': 3267, 'ids': []}]


def f(y):
    y['type'] = [v for v in y['type'] if v not in [6, 7]]
    if len(y['type']) == 0:
        y['type'] = [4]
    return y

index = 0

for each in db:
    pairs = db[each]['QApairs']
    db[each]['QApairs'] = [f(pair) for pair in pairs]
    for i, pair in enumerate(pairs):
        db[each]['QApairs'][i]['id'] = index
        total[pair['type'][0]]['ids'].append(index)
        index += 1


# print(list(map(lambda x: len(x['ids']), total)))
shuffled = list(map(lambda x: random.sample(x, len(x)), [x['ids'] for x in total]))
train_id = reduce(lambda x, y: x + y, [x[:int(len(x) * 0.6)] for x in shuffled])
val_id = reduce(lambda x, y: x + y, [x[int(len(x) * 0.6):int(len(x) * 0.8)] for x in shuffled])
test_id = reduce(lambda x, y: x + y, [x[int(len(x) * 0.8):] for x in shuffled])

json.dump(db, open('qa_pairs_with_id.json', 'w'))

with open('train_id.txt', 'w') as f:
    for each in train_id:
        f.write(str(each) + '\n')

with open('val_id.txt', 'w') as f:
    for each in val_id:
        f.write(str(each) + '\n')

with open('test_id.txt', 'w') as f:
    for each in test_id:
        f.write(str(each) + '\n')

