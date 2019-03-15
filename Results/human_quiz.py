import json
from random import shuffle
import random

def generate_quiz():
    with open('cleaned_db.json', 'r') as f:
        db = json.load(f)

    train = {x: y for x, y in db.items() if y['subset'] == 'training'}
    test = {x: y for x, y in db.items() if y['subset'] == 'testing'}

    k_train = list(train.keys())
    shuffle(k_train)
    k_test = list(test.keys())
    shuffle(k_test)
    k_test += ['surprise_mf!' + x for x in k_test[:90]]

    # random pick QA and multiple choices for quiz
    def picking(k, num=300):
        res = {}
        all_t = {x: 0 for x in range(8)}
        for v in k[:num]:
            ti = {}
            n_sample = 1

            key = v.split('!')[-1]
            url = db[key]['video_url']
            pairs = db[key]['QApairs']
            pairs = random.sample(pairs, n_sample)
            for pair in pairs:
                q = pair['question']
                a = pair['answer']
                alts = pair['alternatives']

                items = [a] + alts

                choices = ['A', 'B', 'C', 'D', 'E']
                shuffle(choices)

                correct = choices[0]
                answers = sorted([choices[i] + '. ' + item for i, item in enumerate(items)])

                ti['question'] = q
                ti['choices'] = answers
                ti['correct'] = correct
                ti['video_url'] = url

                res[v] = ti
                t = pair['type']
                for each in t:
                    all_t[each] += 1

        print(all_t)
        return res

    res_train = picking(k_train)
    res_test = picking(k_test)

    with open('quiz/answers.json', 'w') as f:
        json.dump(res_test, f)

    return res_train


def to_google_doc(res_train=None, train=False, QA=True, num_person=10, amount_per=30):
    if train:
        quizes = res_train
        k = quizes.keys()
        with open('quiz/reference.txt', 'w') as f:
            f.write('300 question-answer pairs for reference. Get a feeling of what these questions are like. You can use search when doing quiz.')
            for each in k:
                ti = quizes[each]
                f.write(ti['question'] + '\n')
                for ans in ti['choices']:
                    f.write(ans + '\n')

                f.write('Correct answer: ' + ti['correct'] + '\n\n')

    else:
        quizes = json.load(open('quiz/answers.json'))
        k = list(quizes.keys())
        QA_tag = 'without' if QA else 'with'
        for i in range(num_person):
            with open('quiz/quiz_' + QA_tag + '_video_' + str(i) + '.txt', 'w') as f:
                f.write('Only one choice is correct. Please put the letter of correct answer after the colons.\n')
                if not QA:
                    f.write('URLs are videos that helps answer the questions.\n')

                f.write('\n')
                for each in k[i*amount_per:(i+1)*amount_per]:
                    ti = quizes[each]
                    if not QA:
                        f.write(ti['video_url'] + '\n')

                    f.write(ti['question'] + '\n')
                    for ans in ti['choices']:
                        f.write(ans + '\n')

                    f.write('Your answer: \n\n')


def check_answer(q_id):
    quizes = json.load(open('quiz/answers.json'))
    db = json.load(open('cleaned_db.json'))

    with open('quiz_answer/' + str(q_id) + '.txt', 'r') as f:
        lines = f.readlines()

    k = [x.split('=')[-1].strip() for x in lines if 'https:' in x]
    correct = []
    print(len(lines))
    for i in range(30):
        q = lines[i * 9 + 4].strip()
        for pair in db[k[i]]['QApairs']:
            if q == pair['question']:
                t = pair['type']

        if q == quizes[k[i]]['question']:
            correct.append((quizes[k[i]]['correct'], t))

        else:
            correct.append((quizes['surprise_mf!' + k[i]]['correct'], t))

    assert(len(correct) == 30)

    answers = [x.split(':')[-1].strip().upper() for x in lines if 'Your answer:' in x]
    cnt = {i: [0, {k:0 for k in range(6)}, {k:0 for k in range(6)}] for i in range(3)}
    for i, tri_ans in enumerate(answers):
        for j, ans in enumerate(tri_ans):
            if ans == correct[i][0]:
                cnt[j][0] += 1
                t = correct[i][1]
                for each in t:
                    index = 3 if each == 6 else each
                    cnt[j][1][index] += 1

            else:
                for each in t:
                    index = 3 if each == 6 else each
                    cnt[j][2][index] += 1
                if j == 2:
                    print(quizes[k[i]])

    return {k: [v[0] / 30, v[1], v[2]] for k, v in cnt.items()}


if __name__ == '__main__':
    # res_train = generate_quiz()
    # to_google_doc(res_train=res_train, train=True)
    # to_google_doc(QA=True)
    # to_google_doc(QA=False)
    from functools import reduce
    correct = [check_answer(i)[0][1] for i in [5]]
    wrong = [check_answer(i)[0][2] for i in [5]]
    def jia(d):
        return reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.items()), d)

    def chu(d):
        return reduce(lambda x, y: dict((k, v / y[k]) for k, v in x.items()), d)

    dui = jia(correct)
    cuo = jia(wrong)
    zong = jia([dui, cuo])
    acc = chu([dui, zong])
    print(acc)
    print(sum(dui.values()) / sum(zong.values()))

