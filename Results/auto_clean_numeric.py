############################
#
# Auto clean numeric QAs
#
############################


import pandas as pd
from nltk.tokenize import RegexpTokenizer
import os
import random

numeric_tokenizer = RegexpTokenizer(r'[0-9]+')
normal_tokenizer = RegexpTokenizer(r"[A-Za-z0-9-']+")
# digit = numeric_tokenizer.tokenize(ans)

rest = [2, 4, 5, 6]

for k in rest:
    name = 'kou' + str(k) + '.csv'
    df = pd.read_csv('clean_assignment' + name)
    # Index(['alt1', 'alt2', 'alt3', 'alt4', 'answer', 'question', 'ytid'], dtype='object')

    for i, row in df.iterrows():
        q = row['question']
        a = row['answer']
        if pd.isna(q):
            continue

        if 'when' in q or 'When' in q or 'time' in q:
            # Questions related to time
            digit = numeric_tokenizer.tokenize(a)
            if len(digit):
                a = digit[0]
                df.set_value(i, 'answer', a)
                for j in range(1, 5):
                    if int(a) <= 50:
                        alt = random.randint(*random.choice([(int(a) + 50, 700)]))
                    elif int(a) >= 650:
                        alt = random.randint(*random.choice([(1, int(a) - 50)]))
                    else:
                        alt = random.randint(*random.choice([(1, int(a) - 50), (int(a) + 50, 700)]))

                    df.set_value(i, 'alt' + str(j), alt)

        if 'many' in q or 'much' in q or 'number' in q:
            # Questions related to counting
            digit = numeric_tokenizer.tokenize(a)
            if len(digit):
                a = digit[0]
                df.set_value(i, 'answer', a)

                alts = list(set(range(6)) - {int(a)})
                random.shuffle(alts)
                alts = alts[:4]

                for j in range(1, 5):
                    df.set_value(i, 'alt' + str(j), alts[j-1])

        if ' or ' in q:
            # Need human force
            print(q)
            print(a)

            alt1 = input('1: ')
            alt2 = input('2: ')
            alt3 = input('3: ')
            alt4 = input('4: ')

            df.set_value(i, 'alt1', alt1)
            df.set_value(i, 'alt2', alt2)
            df.set_value(i, 'alt3', alt3)
            df.set_value(i, 'alt4', alt4)

    df.to_csv('cleaned_' + str(k) + '.csv', index=None)

