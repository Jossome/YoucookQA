import json

with open("youcookii_annotations.json", "r") as f:
    x = json.load(f)

k = list(x['database'].keys())
res = {}
for each in k:
    res[each] = []

for each in k:
    test = x['database'][each]['annotations']
    for seg in test:
        res[each].append(tuple(seg['segment']))

with open('../YouCookII/splits/test_list.txt', 'r') as f:
    tests = f.readlines()

tests = [x.strip().split('/')[-1] for x in tests]

real = {k: res[k] for k in tests}

import pickle
with open('seg_info.pkl', 'wb') as f:
    pickle.dump(real, f)

