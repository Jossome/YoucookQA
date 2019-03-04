import json
from datetime import timedelta
import pandas as pd

with open("youcookii_annotations_trainval.json", "r") as f:
    x = json.load(f)


df_recipe = pd.read_csv('label_foodtype.csv', header=None)
df_recipe.columns = ['typeid', 'recipe']

k = list(x['database'].keys())
csv = {'ytid': [], 'recipe': []}
for i in range(16):
    csv['description' + str(i+1)] = []

for each in k:
    test = x['database'][each]['annotations']
    steps = ''
    for i in range(16):
        if i >= len(test):
            csv['description' + str(i+1)].append(None)
            continue

        ann = test[i]
        csv['description' + str(i+1)].append(str(ann['id']) + '    ' + str(timedelta(seconds=ann['segment'][0])) + '-' + str(timedelta(seconds=ann['segment'][1])) + '    ' + ann['sentence'])

    csv['ytid'].append(each)
    csv['recipe'].append(list(df_recipe[df_recipe['typeid'] == int(x['database'][each]['recipe_type'])]['recipe'])[0])

df = pd.DataFrame(csv)
df[:50].to_csv('batch_sample.csv', index=None)

df_with_start_end = df[:50]
df_with_start_end['start'] = [0] * 50
df_with_start_end['end'] = [100] * 50
df_with_start_end.to_csv('batch_start_end.csv', index=None)

df[:4000].to_csv('batch0.csv', index=None)
df[4000:8000].to_csv('batch1.csv', index=None)
df[8000:12000].to_csv('batch2.csv', index=None)
df[12000:].to_csv('batch3.csv', index=None)
