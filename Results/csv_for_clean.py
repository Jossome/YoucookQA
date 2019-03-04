import pandas as pd
import json
import os

db = json.load(open('qa_with_multiple_choice.json', 'r'))
done_csv = ['db_clean/' + x for x in os.listdir('db_clean')]
done = set()
for each in done_csv:
    df = pd.read_csv(each)
    done |= set(df['Input.ytid'])

df_main = {'ytid': [], 'question': [], 'answer': [], 'alt1': [], 'alt2': [], 'alt3': [], 'alt4': []}
df_kou = {'ytid': [], 'question': [], 'answer': [], 'alt1': [], 'alt2': [], 'alt3': [], 'alt4': []}

for v in db:
    if v in done:
        continue

    pairs = db[v]['QApairs']
    for pair in pairs:
        if 0 in pair['type'] or 3 in pair['type']:
            name = 'df_kou'
        else:
            name = 'df_main'

        vars()[name]['ytid'].append(v)
        vars()[name]['question'].append(pair['question'])
        vars()[name]['answer'].append(pair['answer'])
        vars()[name]['alt1'].append(pair['alternatives'][0])
        vars()[name]['alt2'].append(pair['alternatives'][1])
        vars()[name]['alt3'].append(pair['alternatives'][2])
        vars()[name]['alt4'].append(pair['alternatives'][3])


df_main = pd.DataFrame(df_main, index=None)
# df_kou = pd.DataFrame(df_kou, index=None)
# df_kou[:1000].to_csv('kou0.csv', index=None)
# df_kou[1000:2000].to_csv('kou1.csv', index=None)
# df_kou[2000:3000].to_csv('kou2.csv', index=None)
# df_kou[3000:4000].to_csv('kou3.csv', index=None)
# df_kou[4000:5000].to_csv('kou4.csv', index=None)
# df_kou[5000:6000].to_csv('kou5.csv', index=None)
# df_kou[6000:].to_csv('kou6.csv', index=None)

df_main[:30].to_csv('demo.csv', index=None)
df_main[30:1830].to_csv('main0.csv', index=None)
df_main[1830:3630].to_csv('main1.csv', index=None)
df_main[3630:5430].to_csv('main2.csv', index=None)
df_main[5430:7230].to_csv('main3.csv', index=None)
df_main[7230:].to_csv('main4.csv', index=None)

