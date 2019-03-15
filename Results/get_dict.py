import json
import math
import re
from nltk import word_tokenize
import numpy as np
import pickle
import pandas as pd
import os
from nltk.tokenize import RegexpTokenizer

subset = 'training'

frame_to_second = {}
vid_dura = {}
sampling_sec = 0.5
with open('yc2_duration_frame.csv', 'r') as f:
    for line in f:
        vid_name, vid_dur, vid_frame = [l.strip() for l in line.split(',')]
        frame_to_second[vid_name] = float(vid_dur)*math.ceil(float(vid_frame)*1./float(vid_dur)*sampling_sec)*1./float(vid_frame) # for yc2
        vid_dura[vid_name] = vid_frame


with open('cleaned_db.json', 'r') as f:
    db = json.load(f)

if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('data/' + subset):
    os.makedirs('data/' + subset)

# with open('data/train_list.txt', 'r') as f:
#     train_list = [x.strip().split('/')[-1] for x in f.readlines()]

# with open('data/val_list.txt', 'r') as f:
#     val_list = [x.strip().split('/')[-1] for x in f.readlines()]

# with open('data/test_list.txt', 'r') as f:
#     test_list = [x.strip().split('/')[-1] for x in f.readlines()]

# sort_keys = train_list + val_list + test_list
# db = {k: db_org[k] for k in sort_keys}
# val_first = val_list[0]
# test_first = test_list[0]

set_q = set()
set_a = set()
set_d = set()
set_c = set()
set_all = set()
set_kspace = set()
df_recipe = pd.read_csv('../label_foodtype.csv', header=None, names=['id', 'name'], index_col=0)
recipe = {k: v['name'] for k, v in df_recipe.iterrows()}
# wiki = json.load(open('../wiki.json', 'r'))

max_len_q = 0
max_len_a = 0
max_len_d = 0
max_len_c = 0
num = 0
for each in db:
    pairs = db[each]['QApairs']
    segs = db[each]['annotations']

    for pair in pairs:
        if db[each]['subset'] == subset:
            num += 1
        q = pair['question'].lower()
        a = pair['answer'].lower()
        alts = pair['alternatives']

        token_q = word_tokenize(q)
        set_q |= set(token_q)
        token_a = word_tokenize(a)

        # fuck classes for each answer
        temp = a
        if token_a[0] == 'yes':
            temp = 'Yes.'
        if token_a[0] == 'no':
            temp = 'No.'
        set_kspace |= {temp}

        set_a |= set(token_a)
        for alt in alts:
            token_a = word_tokenize(alt.lower())
            set_a |= set(token_a)

        max_len_q = max(len(token_q), max_len_q)
        max_len_a = max(len(token_a), max_len_a)

    for seg in segs:
        desc = seg['sentence']
        token_d = word_tokenize(desc)
        set_d |= set(token_d)
        max_len_d = max(len(token_d), max_len_d)

        cc = ' '.join([x['text'] for x in seg['transcripts']])
        token_c = word_tokenize(cc)
        set_c |= set(token_c)
        max_len_c = max(len(token_c), max_len_c)

set_all = set_q | set_a | set_d | set_c
# set_wiki = set()
# max_len_wiki = 0
# for each in wiki:
#     token = word_tokenize(wiki[each])
#     set_wiki |= set(token)
#     max_len_wiki = max(len(token), max_len_wiki)

dict_q = {}
dict_a = {}
dict_d = {}
dict_c = {}
dict_all = {}
dict_kspace = {}
# dict_wiki = {}
for i, each in enumerate(sorted(list(set_q))):
    dict_q[each] = i + 1

for i, each in enumerate(sorted(list(set_a))):
    dict_a[each] = i + 1

for i, each in enumerate(sorted(list(set_d))):
    dict_d[each] = i + 1

for i, each in enumerate(sorted(list(set_c))):
    dict_c[each] = i + 1

for i, each in enumerate(sorted(list(set_all))):
    dict_all[each] = i + 1

for i, each in enumerate(sorted(list(set_kspace))):
    dict_kspace[each] = i + 1

# for i, each in enumerate(sorted(list(set_wiki))):
#     dict_wiki[each] = i + 1

with open('data/dict_q.json', 'w') as f:
    json.dump(dict_q, f)

with open('data/dict_a.json', 'w') as f:
    json.dump(dict_a, f)

with open('data/dict_d.json', 'w') as f:
    json.dump(dict_d, f)

with open('data/dict_c.json', 'w') as f:
    json.dump(dict_c, f)

with open('data/dict_all.json', 'w') as f:
    json.dump(dict_all, f)

with open('data/dict_kspace.json', 'w') as f:
    json.dump(dict_kspace, f)

# with open('data/dict_wiki.json', 'w') as f:
#     json.dump(dict_wiki, f)

# fuck matrix
mat_q = np.zeros((num, max_len_q))
mat_a = np.zeros((num, 5, max_len_a))
mat_d = np.zeros((num, 17, max_len_d))
mat_c = np.zeros((num, 17, max_len_c))
mat_q_uniform = np.zeros((num, max_len_q))
mat_a_uniform = np.zeros((num, 5, max_len_a))
mat_d_uniform = np.zeros((num, 17, max_len_d))
mat_c_uniform = np.zeros((num, 17, max_len_c))
mat_kspace = np.zeros(num)
# mat_wiki = np.zeros((num, max_len_wiki))
mat_id = ['' for x in range(num)]
mat_type = np.zeros(num)
mat_ans_type = np.zeros(num)
mat_frame = -np.ones((num, 17))

num_list = {
    'none': 0,
    'zero': 0,
    'once': 1,
    'one': 1,
    'twice': 2,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20
}

def process(word):
    if word.lower() in num_list:
        return str(num_list[word.lower()])
    else:
        return word.lower()

i = 0
ynq = 0
for each in db:
    # if each == val_first:
    #     print('train last:', i)

    # if each == test_first:
    #     print('val last:', i)

    if db[each]['subset'] != subset:
        continue

    pairs = db[each]['QApairs']
    length = db[each]['duration']
    segs = db[each]['annotations']
    name = recipe[int(db[each]['recipe_type'])]
    name = re.sub(r'\s+', '_', name)
    # intro = wiki[name]
    # token = word_tokenize(intro)

    for pair in pairs:

        q = pair['question'].lower()

        # four answer types: ynq:0, numq:1, sinq:2, texq:3
        a = pair['answer']
        normal_tokenizer = RegexpTokenizer(r'[A-Za-z0-9-]+')
        numeric_tokenizer = RegexpTokenizer(r'[0-9-]+')
        token_a = normal_tokenizer.tokenize(a)
        a = (' ').join([process(x) for x in token_a])
        token_a = normal_tokenizer.tokenize(a)
        digit_a = numeric_tokenizer.tokenize(a)
        try:
            if token_a[0].lower() in ['yes', 'no']:
                # ynq += 1
                mat_ans_type[i] = 0
            elif len(digit_a) > 0:
                # numq += 1
                mat_ans_type[i] = 1
            elif len(token_a) == 1:
                # sinq += 1
                mat_ans_type[i] = 2
            else:
                # texq += 1
                mat_ans_type[i] = 3
        except Exception as e:
            # print(len(pair['question'].strip()))
            # Strange that len is much greater than zero,
            # and not blank, but won't print a single char.
            mat_ans_type[i] = 3

        a = []
        a.append(pair['answer'].lower())
        for alt in pair['alternatives']:
            a.append(alt.lower())

        t = pair['type']
        token_q = word_tokenize(q)
        for j, seg in enumerate(segs):
            mat_frame[i][j] = int(seg['segment'][0] / frame_to_second[each])

            desc = seg['sentence']
            token_d = word_tokenize(desc)
            for k, word in enumerate(token_d):
                mat_d[i][j][k] = dict_d[word]
                mat_d_uniform[i][j][k] = dict_all[word]

            cc = ' '.join([x['text'] for x in seg['transcripts']])
            token_c = word_tokenize(cc)
            for k, word in enumerate(token_c):
                mat_c[i][j][k] = dict_c[word]
                mat_c_uniform[i][j][k] = dict_all[word]

        # for j, word in enumerate(token):
        #     mat_wiki[i][j] = dict_wiki[word]

        for j, word in enumerate(token_q):
            mat_q[i][j] = dict_q[word]
            mat_q_uniform[i][j] = dict_all[word]

        for j, alt in enumerate(a):
            token_a = word_tokenize(alt)
            temp = alt
            if token_a[0] == 'yes':
                temp = 'yes'
                ynq += 1
            if token_a[0] == 'no':
                temp = 'no'
                ynq -= 1
            token_a = word_tokenize(temp)
            for k, word in enumerate(token_a):
                mat_a[i][j][k] = dict_a[word]
                mat_a_uniform[i][j][k] = dict_all[word]

        mat_id[i] = each
        mat_type[i] = t[0]

        token_a = word_tokenize(pair['answer'].lower())
        temp = pair['answer'].lower()
        if token_a[0] == 'yes':
            temp = 'Yes.'
        if token_a[0] == 'no':
            temp = 'No.'
        mat_kspace[i] = dict_kspace[temp]

        i += 1

print(ynq)

with open('data/' + subset + '/mat_q.pkl', 'wb') as f:
    pickle.dump(mat_q, f, protocol=2)

with open('data/' + subset + '/mat_a.pkl', 'wb') as f:
    pickle.dump(mat_a, f, protocol=2)

with open('data/' + subset + '/mat_d.pkl', 'wb') as f:
    pickle.dump(mat_d, f, protocol=2)

with open('data/' + subset + '/mat_c.pkl', 'wb') as f:
    pickle.dump(mat_c, f, protocol=2)

with open('data/' + subset + '/mat_q_uniform.pkl', 'wb') as f:
    pickle.dump(mat_q_uniform, f, protocol=2)

with open('data/' + subset + '/mat_a_uniform.pkl', 'wb') as f:
    pickle.dump(mat_a_uniform, f, protocol=2)

with open('data/' + subset + '/mat_d_uniform.pkl', 'wb') as f:
    pickle.dump(mat_d_uniform, f, protocol=2)

with open('data/' + subset + '/mat_c_uniform.pkl', 'wb') as f:
    pickle.dump(mat_c_uniform, f, protocol=2)

with open('data/' + subset + '/mat_id.pkl', 'wb') as f:
    pickle.dump(mat_id, f, protocol=2)

with open('data/' + subset + '/mat_type.pkl', 'wb') as f:
    pickle.dump(mat_type, f, protocol=2)

with open('data/' + subset + '/mat_ans_type.pkl', 'wb') as f:
    pickle.dump(mat_ans_type, f, protocol=2)

with open('data/' + subset + '/mat_kspace.pkl', 'wb') as f:
    pickle.dump(mat_kspace, f, protocol=2)

# with open('data/' + subset + '/mat_wiki.pkl', 'wb') as f:
#     pickle.dump(mat_wiki, f, protocol=2)

with open('data/' + subset + '/mat_frame.pkl', 'wb') as f:
    pickle.dump(mat_frame, f, protocol=2)
