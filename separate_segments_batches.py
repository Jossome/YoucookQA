import json
import pandas as pd
from random import shuffle

with open("youcookii_annotations.json", "r") as f:
    x = json.load(f)

df_recipe = pd.read_csv('label_foodtype.csv', header=None)
df_recipe.columns = ['typeid', 'recipe']


k_all = list(x['database'].keys())
with open('Results/done.txt', 'r') as f:
    k_done = f.readlines()
k_done = [x.strip() for x in k_done]
# k = list(set(k_all) - set(k_done))
k = k_all
shuffle(k)

print(len(k))
csv = {'ytid': [], 'recipe': []}
for i in range(16):
    csv['description' + str(i+1)] = []
    csv['start' + str(i+1)] = []
    csv['end' + str(i+1)] = []

for each in k:
    test = x['database'][each]['annotations']
    steps = ''
    for i in range(16):
        if i >= len(test):
            csv['description' + str(i+1)].append('')
            csv['start' + str(i+1)].append(0)
            csv['end' + str(i+1)].append(0)
            continue

        ann = test[i]
        csv['description' + str(i+1)].append(str(ann['id'] + 1) + '    ' + ann['sentence'])
        csv['start' + str(i+1)].append(ann['segment'][0])
        csv['end' + str(i+1)].append(ann['segment'][1])

    csv['ytid'].append(each)
    csv['recipe'].append(list(df_recipe[df_recipe['typeid'] == int(x['database'][each]['recipe_type'])]['recipe'])[0])

df = pd.DataFrame(csv)
df = df.sample(frac=1)
df[:50].to_csv('test.csv', index=None)
df[50:1000].to_csv('random.csv', index=None)
