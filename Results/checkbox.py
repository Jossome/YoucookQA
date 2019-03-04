import pandas as pd
import os
if os.path.exists('reasoning/with_checkbox.csv'):
    df = pd.read_csv('reasoning/with_checkbox.csv')
else:
    with open('checkpoint.log', 'w') as f:
        f.write('0,1')
    df = pd.read_csv('reasoning/no-check.csv')
    tmp = pd.read_csv('reasoning/Batch_3316434_batch_results.csv')
    checkbox = set(tmp.columns) - set(df.columns)
    for each in checkbox:
        df[each] = ['' for x in range(len(df))]

with open('checkpoint.log', 'r') as f:
    text = f.readline().split(',')
    i_new = int(text[0])
    q_new = int(text[1])

tmp = df[:]
for i, row in tmp.iterrows():
    if i < i_new:
        continue

    print(i, 'th video')
    if row['Answer.q1'] and row['Answer.a1']:
        if i == i_new and q_new > 1:
            pass
        else:
            print(row['Answer.q1'])
            print(row['Answer.a1'])
            prop = input('change of property: ')
            count = input('counting number: ')
            when = input('locating time point: ')
            dura = input('duration: ')
            order = input('action order: ')
            if prop:
                df.loc[i, 'Answer.t21'] = 'on'
            if count:
                df.loc[i, 'Answer.t31'] = 'on'
            if when:
                df.loc[i, 'Answer.t41'] = 'on'
            if dura:
                df.loc[i, 'Answer.t51'] = 'on'
            if order:
                df.loc[i, 'Answer.t61'] = 'on'

            end = input('wanna end?[y/n]: ')
            while not end:
                end = input('wanna end?[y/n]: ')

            df.to_csv('reasoning/with_checkbox.csv', index=None)
            with open('checkpoint.log', 'w') as f:
                f.write(str(i) + ',2')

            if end == 'y':
                break


    if row['Answer.q2'] and row['Answer.a2']:
        if i == i_new and q_new > 2:
            pass
        else:
            print(row['Answer.q2'])
            print(row['Answer.a2'])
            prop = input('change of property: ')
            count = input('counting number: ')
            when = input('locating time point: ')
            dura = input('duration: ')
            order = input('action order: ')
            if prop:
                df.loc[i, 'Answer.t22'] = 'on'
            if count:
                df.loc[i, 'Answer.t32'] = 'on'
            if when:
                df.loc[i, 'Answer.t42'] = 'on'
            if dura:
                df.loc[i, 'Answer.t52'] = 'on'
            if order:
                df.loc[i, 'Answer.t62'] = 'on'

            end = input('wanna end?[y/n]: ')
            while not end:
                end = input('wanna end?[y/n]: ')

            df.to_csv('reasoning/with_checkbox.csv', index=None)
            with open('checkpoint.log', 'w') as f:
                f.write(str(i) + ',3')

            if end == 'y':
                break

    if row['Answer.q3'] and row['Answer.a3']:
        print(row['Answer.q3'])
        print(row['Answer.a3'])
        prop = input('change of property: ')
        count = input('counting number: ')
        when = input('locating time point: ')
        dura = input('duration: ')
        order = input('action order: ')
        if prop:
            df.loc[i, 'Answer.t23'] = 'on'
        if count:
            df.loc[i, 'Answer.t33'] = 'on'
        if when:
            df.loc[i, 'Answer.t43'] = 'on'
        if dura:
            df.loc[i, 'Answer.t53'] = 'on'
        if order:
            df.loc[i, 'Answer.t63'] = 'on'

        end = input('wanna end?[y/n]: ')
        while not end:
            end = input('wanna end?[y/n]: ')

        df.to_csv('reasoning/with_checkbox.csv', index=None)
        with open('checkpoint.log', 'w') as f:
            f.write(str(i+1) + ',1')

        if end == 'y':
            break

df.to_csv('reasoning/with_checkbox.csv', index=None)

