import json
import pandas as pd
from random import shuffle
import os

with open("../youcookii_annotations.json", "r") as f:
    x = json.load(f)

k = list(x['database'].keys())

types = {'count': 0,
        'order': 1,
        'taste': 2,
        'when': 3,
        'reasoning': 4,
        'property': 5,
        'duration': 6,
        'freestyle': 7}

def get_type(row, q_num):
    res = [4]
    t2 = 'Answer.t2' + str(q_num)
    if t2 in row.index and row[t2] == 'on':
        res.append(types['property'])
    t3 = 'Answer.t3' + str(q_num)
    if t3 in row.index and row[t3] == 'on':
        res.append(types['count'])
    t4 = 'Answer.t4' + str(q_num)
    if t4 in row.index and row[t4] == 'on':
        res.append(types['when'])
    t5 = 'Answer.t5' + str(q_num)
    if t5 in row.index and row[t5] == 'on':
        res.append(types['duration'])
    t6 = 'Answer.t6' + str(q_num)
    if t6 in row.index and row[t6] == 'on':
        res.append(types['order'])
    t7 = 'Answer.t7' + str(q_num)
    if t7 in row.index and row[t7] == 'on':
        res.append(types['taste'])

    if len(res) == 1:
        res.append(7)
    return res

for each in k:
    x['database'][each]['QApairs'] = []
db = x['database']

csvs = ['QAcollection/count/' + x for x in os.listdir('count')]\
    + ['QAcollection/order/' + x for x in os.listdir('order')]\
    + ['QAcollection/reasoning/' + x for x in os.listdir('reasoning') if x[0] == 'B']\
    + ['QAcollection/taste/' + x for x in os.listdir('taste')]\
    + ['QAcollection/property/' + x for x in os.listdir('property')]\
    + ['QAcollection/duration/' + x for x in os.listdir('duration')]\
    + ['QAcollection/when/' + x for x in os.listdir('when')]

cnt = 0
for csv in csvs:
    q_type = [types[csv.split('/')[0]]]
    df = pd.read_csv(csv)
    df = df[df['AssignmentStatus'] == 'Approved']
    for index, row in df.iterrows():
        key = row['Answer.ytid']
        if q_type[0] == types['property']:
            q_type = [types['property'], types['reasoning']]
        elif q_type[0] == types['reasoning']:
            q_type = get_type(row, 1)

        if row['Answer.q1'] != '{}' and row['Answer.a1'] != '{}':
            if q_type[-1] != 7:
                db[key]['QApairs'].append({'question': row['Answer.q1'], 'answer': row['Answer.a1'], 'type': q_type})
                cnt += 1
        if 'Answer.q2' in df.columns:
            if row['Answer.q2'] != '{}' and row['Answer.a2'] != '{}':
                q_type = get_type(row, 2)
                if q_type[-1] != 7:
                    db[key]['QApairs'].append({'question': row['Answer.q2'], 'answer': row['Answer.a2'], 'type': q_type})
                    cnt += 1
            if row['Answer.q3'] != '{}' and row['Answer.a3'] != '{}':
                q_type = get_type(row, 3)
                if q_type[-1] != 7:
                    db[key]['QApairs'].append({'question': row['Answer.q3'], 'answer': row['Answer.a3'], 'type': q_type})
                    cnt += 1

print(cnt)

with open('qapairs.json', 'w') as f:
    json.dump(db, f)
