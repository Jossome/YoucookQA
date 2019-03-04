import json
import pandas as pd
import copy
import os


def count(db):
    cnt = 0
    lent = 0
    for each in db:
        pairs = db[each]['QApairs']
        for pair in pairs:
            if 'alternatives' not in pair:
                cnt += 1
        lent += len(pairs)

    return cnt, lent


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


types = {'count': 0,
        'order': 1,
        'taste': 2,
        'when': 3,
        'reasoning': 4,
        'property': 5,
        'duration': 6,
        'freestyle': 7}

cnt = 0  # count qa cleaned
deleted = []
db_org = json.load(open('qa_with_multiple_choice.json', 'r'))
db = copy.deepcopy(db_org)

d = 'clean_result/named_csvs'
files = os.listdir(d)
for f in files:
    num = f.split('.')[0]
    path_cln = os.path.join(d, f)
    path_org = 'clean_assignment/main_' + num + '.csv'
    df_cln = pd.read_csv(path_cln)
    df_org = pd.read_csv(path_org)

    '''
    # print(df_cln.columns)
        Index(['HITId', 'HITTypeId', 'Title', 'Description', 'Keywords', 'Reward',
           'CreationTime', 'MaxAssignments', 'RequesterAnnotation',
           'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds',
           'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds',
           'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime',
           'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime',
           'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate',
           'Last30DaysApprovalRate', 'Last7DaysApprovalRate', 'Input.alt1',
           'Input.alt2', 'Input.alt3', 'Input.alt4', 'Input.answer',
           'Input.question', 'Input.ytid', 'Answer.alt1', 'Answer.alt2',
           'Answer.alt3', 'Answer.alt4', 'Answer.ans', 'Answer.delete',
           'Answer.edit_alters', 'Answer.edit_answer', 'Approve', 'Reject'],
        dtype='object')

    # print(df_org.columns)
        Index(['alt1', 'alt2', 'alt3', 'alt4', 'answer', 'question', 'ytid'], dtype='object')
    '''

    # Pre-checking
    # shabi = False
    # for each in df_cln['Input.question']:
    #     if each not in list(df_org['question']):
    #         shabi = True

    # for each in df_cln['Input.ytid']:
    #     if each not in list(df_org['ytid']):
    #         shabi = True

    # assert(shabi == False)
    # if (len(df_org) != len(set(zip(df_org['question'], df_org['ytid'])))):
    #     print(d, f)
    #     print(len(df_org), len(set(zip(df_org['question'], df_org['ytid']))))

    wrong = []  # To store QAs with missing ytid

    # TODO: Need to check if approved.
    for _, row in df_cln.iterrows():

        # Check if delete
        if 'Answer.delete' in df_cln.columns:
            if row['Answer.delete'] == 'on':
                deleted.append(row)
                continue

        # There might be 'nan' ytid
        # Add them to a 'wrong' list
        ytid = row['Input.ytid']
        if pd.isna(ytid):
            wrong.append(row)
            continue

        # Check if correct answer has been modified
        que = row['Input.question']
        if 'Answer.edit_answer' in df_cln.columns:
            ans = row['Answer.ans'] if row['Answer.edit_answer'] == 'on' else row['Input.answer']
        else:
            ans = row['Input.answer']

        # Get modified alternatives
        alt = []
        for i in range(4):
            if 'Answer.edit_answer' in df_cln.columns:
                if row['Answer.alt' + str(i+1)] == '{}':
                    alt.append(row['Input.alt' + str(i+1)])
                else:
                    alt.append(row['Answer.alt' + str(i+1)])
            else:
                alt.append(row['Input.alt' + str(i+1)])


        # Use origin db as ref, modify on copied db
        pairs = db_org[ytid]['QApairs']
        no_pair = True
        for j, pair in enumerate(pairs):
            if que in pair['question'] or pair['question'] in que:
                no_pair = False
                db[ytid]['QApairs'][j]['answer'] = ans
                db[ytid]['QApairs'][j]['alternatives'] = alt

        if no_pair:  # Mostly the manually checkboxed ones
            found = False
            csvs = ['QAcollection/reasoning/Batch_addon.csv', 'QAcollection/duration/Batch_3356616_batch_results.csv', 'QAcollection/duration/Batch_3358631_batch_results.csv']
            for csv in csvs:
                q_type = [types[csv.split('/')[1]]]
                df = pd.read_csv(csv)
                df = df[df['AssignmentStatus'] == 'Approved']
                for _, local_row in df.iterrows():
                    key = local_row['Answer.ytid']
                    if ytid == key:
                        if que == local_row['Answer.q1']:
                            found = True
                            if q_type[0] == types['reasoning']:
                                q_type = get_type(local_row, 1)

                            if q_type[-1] != 7:
                                db[ytid]['QApairs'].append({'question': que, 'answer': ans, 'alternatives':alt, 'type': q_type})

                        if 'Answer.q2' in df.columns:
                            if que == local_row['Answer.q2']:
                                found = True
                                q_type = get_type(local_row, 2)
                                if q_type[-1] != 7:
                                    db[ytid]['QApairs'].append({'question': que, 'answer': ans, 'alternatives':alt, 'type': q_type})

                            if que == local_row['Answer.q3']:
                                found = True
                                q_type = get_type(local_row, 3)
                                if q_type[-1] != 7:
                                    db[ytid]['QApairs'].append({'question': que, 'answer': ans, 'alternatives':alt, 'type': q_type})

            if not found:
                wrong.append(row)

    # Deal with wrong ytid (nan)
    local_set = set([x for x in df_cln['Input.ytid'] if not pd.isna(x)])
    for each in wrong:
        que = each['Input.question']
        if pd.isna(que):
            continue

        ytid = each['Input.ytid']
        if ytid in local_set:
            pairs = db_org[ytid]['QApairs']
            no_pair = True
            gotcha = ''
            for j, pair in enumerate(pairs):
                if que in pair['question'] or pair['question'] in que:
                    no_pair = False
                    gotcha = ytid
                    db[ytid]['QApairs'][j]['answer'] = ans
                    db[ytid]['QApairs'][j]['alternatives'] = alt

            if no_pair:
                cnt += 1
                if gotcha:
                    pass
                    # db[gotcha]['QApairs'].append({'question': que, 'answer': ans, 'alternatives': alt})

        else:
            found = False
            no_pair = True
            gotcha = ''
            for ytid in db_org:
                pairs = db_org[ytid]['QApairs']
                for j, pair in enumerate(pairs):
                    if que in pair['question'] or pair['question'] in que:
                        found = True
                        no_pair = False
                        gotcha = ytid
                        db[ytid]['QApairs'][j]['answer'] = ans
                        db[ytid]['QApairs'][j]['alternatives'] = alt

            if no_pair:
                cnt += 1
                if gotcha:
                    pass
                    # db[gotcha]['QApairs'].append({'question': que, 'answer': ans, 'alternatives': alt})

            if not found:
                print('malegebi')

# Deal with deleted items
for each in deleted:
    ytid = each['Input.ytid']

    def determine(x):
        if x['question'] in each['Input.question'] or each['Input.question'] in x['question']:
            return False

        return True

    if not pd.isna(ytid):
        db[ytid]['QApairs'] = [x for x in db[ytid]['QApairs'] if determine(x)]

print(count(db))
with open('cleaned_db.json', 'w') as f:
    json.dump(db, f)
