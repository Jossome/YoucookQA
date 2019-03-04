import json
import random
import nltk
import re

def preprocess(sentence):
    res = sentence[:]
    res = re.sub(r'pre ', r'pre', res)
    return res


def split_by_and(sentence):
    res = []
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    indices = [i for i, x in enumerate(tokens) if x == 'and']
    if len(indices) == 0:
        return ['they ' + sentence]

    for i in indices:
        if len(tagged) == i + 1:
            head = 'they ' + (' ').join(tokens[:i])
            res.append(head)
            return res
        if tagged[i + 1][1][0] == 'V':
            head = 'they ' + (' ').join(tokens[:i])
            tail = (' ').join(tokens[i + 1:])
            res.append(head)
            return res + split_by_and(tail)

    res.append('they ' + sentence)
    return res


with open("youcookii_annotations.json", "r") as f:
    x = json.load(f)

k = list(x['database'].keys())
final_list = {'videos': []}

for each in k:

    tmp = x['database'][each]
    sub_desc = []

    for ann in tmp['annotations']:
        sub_desc += split_by_and(preprocess(ann['sentence']))

    pick_i = random.randint(0, len(sub_desc) - 1)
    question = 'When did ' + sub_desc[pick_i] + '?'
    if pick_i == 0:
        alts = ['before', 'before', 'begin']
    elif pick_i == len(sub_desc) - 1:
        alts = ['after', 'after', 'last']
    else:
        alts = ['before', 'before', 'after', 'after', 'between']

    ans_form = random.choice(alts)
    answer = ''
    if ans_form == 'before':
        answer = 'Before ' + sub_desc[pick_i + 1] + '.'
    if ans_form == 'after':
        answer = 'After ' + sub_desc[pick_i - 1] + '.'
    if ans_form == 'between':
        answer = 'Between ' + sub_desc[pick_i - 1] + ' and ' + sub_desc[pick_i + 1] + '.'
    if ans_form == 'begin':
        answer = 'In the beginning.'
    if ans_form == 'last':
        answer = 'At last.'


    pair = {'id': ann['id'], 'question': question, 'answer': answer}
    final_list['videos'].append(pair)

print(final_list)
with open('when_QA.json', 'w') as f:
    json.dump(final_list, f)
