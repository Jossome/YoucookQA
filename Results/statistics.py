import pandas as pd
import os
import re
import json
import pickle
import collections
import random
import copy
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class statistics:
    def __init__(self, cleaned=True):
        if cleaned:
            self.types = {
                'total': -1,
                'count': 0,
                'order': 1,
                'taste': 2,
                'when': 3,
                'reasoning': 4,
                'property': 5,
                'duration': 6,
                'freestyle': 7
            }
            self.db = json.load(open('cleaned_db.json', 'r'))
            def f(x):
                y = copy.deepcopy(x)
                y['type'] = [v for v in y['type'] if v not in [6, 7]]
                return y

            for each in self.db:
                pairs = self.db[each]['QApairs']
                self.db[each]['QApairs'] = [f(pair) for pair in pairs]

        else:
            self.db = json.load(open('qapairs.json', 'r'))

        # self.dict_a = json.load(open('dict_a.json', 'r'))
        df_recipe = pd.read_csv('../label_foodtype.csv', header=None, names=['id', 'name'], index_col=0)
        self.recipe = {v['name']: k for k, v in df_recipe.iterrows()}
        self.recipe_id_key = {v: k for k, v in self.recipe.items()}
        self.recipe['total'] = -1

        self.num_list = {
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


    def check_comlete(self, folder):
        assert(folder in ['count', 'order', 'reasoning', 'taste', 'when', 'property', 'duration'])
        files = os.listdir(folder)

        dfs = []

        for csv in files:
            path = folder + '/' + csv
            df = pd.read_csv(path)
            df = df[df['AssignmentStatus'] == 'Approved']
            dfs.append(df)

        df = pd.concat(dfs)
        done = set(df['Answer.ytid'])
        if len(done) == 2000:
            print(folder + ' complete.')
            return

        with open('done_' + folder + '.txt', 'w') as f:
            for each in done:
                f.write(each + '\n')
        print(folder + ' with ' + str(2000 - done) + ' incomplete.')


    def get_frequent_answers(type_name):
        mat_a = pickle.load(open('mat_a.pkl', 'rb'))
        mat_type = pickle.load(open('mat_type.pkl', 'rb'))
        type_num = self.types[type_name]
        # type_num == -1 then whole dataset
        if type_num == -1:
            mat_reason = [mat_a[i] for i in range(len(mat_type))]
        else:
            mat_reason = [mat_a[i] for i in range(len(mat_type)) if mat_type[i] == type_num]

        inv_dict_a = {v: k for k, v in self.dict_a.items()}
        inv_dict_a[0] = ''

        # sent for sentence
        sent_a = [','.join([str(int(word)) for word in x]) for x in mat_reason]

        cnt = collections.Counter(sent_a)

        res = sorted(cnt.items(), key=lambda x:x[1])
        for sentence, count in res:
            sent = sentence.split(',')
            sent = [inv_dict_a[int(x)] for x in sent]
            print(sent, count)

        print(len(mat_reason))


    def process(self, word):
        if word.lower() in self.num_list:
            return str(self.num_list[word.lower()])
        else:
            return word.lower()


    def tag_type(self, *args):
        # type_num: we want
        # types: present
        type_num = args[0]
        types = args[1]

        if type_num != -1:
            if type_num not in types:
                return True

        return False


    def recipe_type(self, *args):
        # recipe_num: we want
        # recipe_type: present
        recipe_num = args[0]
        recipe_type = args[2]

        if recipe_num != -1:
            if recipe_num != recipe_type:
                return True

        return False


    def get_stats(self, condition, para):
        # get the stats of para, with condition func.
        cnt = 0
        tags = 0
        words = 0
        ynq = 0
        numq = 0
        sinq = 0
        texq = 0

        caonima = 0
        for each in self.db:
            pairs = self.db[each]['QApairs']
            if self.db[each]['subset'] != 'validation':
                continue

            for pair in pairs:
                t = pair['type']
                if condition(para, t, int(self.db[each]['recipe_type'])):
                    # if this qa pair is what we want.
                    continue

                tags += len(t)
                cnt += 1

                a = pair['answer']
                normal_tokenizer = RegexpTokenizer(r'[A-Za-z0-9-]+')
                numeric_tokenizer = RegexpTokenizer(r'[0-9-]+')

                token_a = normal_tokenizer.tokenize(a)
                words += len(token_a)
                a = (' ').join([self.process(x) for x in token_a])
                token_a = normal_tokenizer.tokenize(a)
                digit_a = numeric_tokenizer.tokenize(a)
                try:
                    if token_a[0].lower() in ['yes', 'no']:
                        ynq += 1
                    elif len(digit_a) > 0:
                        numq += 1
                    elif len(token_a) == 1:
                        sinq += 1
                    else:
                        texq += 1
                except Exception as e:
                    # print(len(pair['question'].strip()))
                    # Strange that len is much greater than zero,
                    # and not blank, but won't print a single char.
                    caonima += 1

        return cnt, tags, words, ynq, numq, sinq, texq, caonima


    def qa_stats(self, type_name):
        type_num = self.types[type_name]
        # type_num == -1 then whole dataset
        # Yes/No, Num, single word, text
        # Tags/QA-pair, avg word per answer, qa/video

        cnt, tags, words, ynq, numq, sinq, texq, caonima = self.get_stats(self.tag_type, type_num)

        print(type_name)
        print('qapairs: ', cnt)
        print('yes/no: ', ynq)
        print('numeric: ', numq)
        print('single: ', sinq)
        print('text: ', texq)
        print('tags/qa: ', tags / cnt)
        print('ans avg len: ', words / cnt)
        print('qa/video: ', cnt / 2000)
        if type_num == -1:
            print('qa/recipe: ', cnt / 110)
        print('caonima: ', caonima)


    def recipe_stats(self, recipe_name, verbose=True):
        # stats per recipe
        recipe_num = self.recipe[recipe_name]
        cnt, tags, words, ynq, numq, sinq, texq, caonima = self.get_stats(self.recipe_type, recipe_num)

        if verbose:
            print(recipe_name)
            print('qapairs: ', cnt)
            print('yes/no: ', ynq)
            print('numeric: ', numq)
            print('single: ', sinq)
            print('text: ', texq)
            print('tags/qa: ', tags / cnt)
            print('ans avg len: ', words / cnt)
            if recipe_num == -1:
                print('qa/recipe: ', cnt / 110)
            print('caonima: ', caonima)
            print()

        return cnt, tags, words, ynq, numq, sinq, texq


    def get_alternatives(self, tag, recipe):
        res = []
        for each in self.db:
            if self.db[each]['recipe_type'] == recipe or recipe == '000':
                pairs = self.db[each]['QApairs']
                for pair in pairs:
                    if tag in pair['type']:
                        res.append(pair['answer'])

        return res


    def most_similar(self, num, alts, src):
        # get $num most similar alternatives in alts to src
        doc = tuple([src] + list(alts-{src}))
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(doc)
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

        # doc_sim does not contain src answer
        doc_sim = sorted(zip(doc[1:], sim[0][1:]), key=lambda x: x[1])

        if list(sim[0]).count(0) == len(sim[0]):
            # This is a numeric answer
            tmp = list(alts)
            random.shuffle(tmp)
            numeric_tokenizer = RegexpTokenizer(r'[0-9-]+')
            res = []
            i = 0
            while len(res) < num and i < len(tmp):
                digit_a = numeric_tokenizer.tokenize(tmp[i])
                if len(digit_a) in [1,2,3,4]:
                    res.append(tmp[i])
                i += 1

            if len(res) < num:
                leftover = list(alts - set(res))
                random.shuffle(leftover)
                res += leftover[:num-len(res)]

        else:
            res = [x[0] for x in doc_sim[:num]]

        return res


    def rand_num_in_sentence(self, ans):
        numeric_tokenizer = RegexpTokenizer(r'[0-9]+')
        result = []
        digit = numeric_tokenizer.tokenize(ans)
        candidates = set(range(1, len(digit) * 10)) - {int(x) for x in digit}
        replace = random.sample(candidates, len(digit) * 4)
        replace1 = [str(x) for x in replace[:len(digit)]]
        result.append(re.sub(r'\d+', lambda m, i=iter(replace1): next(i), ans))
        replace2 = [str(x) for x in replace[len(digit):2 * len(digit)]]
        result.append(re.sub(r'\d+', lambda m, i=iter(replace2): next(i), ans))
        replace3 = [str(x) for x in replace[2 * len(digit):3 * len(digit)]]
        result.append(re.sub(r'\d+', lambda m, i=iter(replace3): next(i), ans))
        replace4 = [str(x) for x in replace[3 * len(digit):]]
        result.append(re.sub(r'\d+', lambda m, i=iter(replace4): next(i), ans))
        return result


    def rule_based_multiple_choice(self):
        # if yes/no, then no/yes
        # if numeric, then numeric
        # if before/after, then after/before
        # if verb + noun, then same verb/same noun/same both
        # don't care bout recipes. FOR NOW.
        normal_tokenizer = RegexpTokenizer(r"[A-Za-z0-9-']+")
        numeric_tokenizer = RegexpTokenizer(r'[0-9]+')

        # first we get all preprocessed answers as set in the db
        # numeric words to arabic numbers
        # yes/no answers to solely yes and no
        answers = []
        for each in self.db:
            pairs = self.db[each]['QApairs']
            for pair in pairs:
                a = pair['answer']
                a = re.sub(r'-', ' - ', a)
                token_a = normal_tokenizer.tokenize(a)
                a = (' ').join([self.process(x) for x in token_a])

                if token_a[0].lower() == 'yes':
                    a = 'yes'
                if token_a[0].lower() == 'no':
                    a = 'no'

                answers.append(a)
        answers = set(answers)

        # then all numeric answers
        numeric = []
        for a in answers:
            digit_a = numeric_tokenizer.tokenize(a)
            if len(digit_a) > 0:
                numeric.append(a)
        numeric = set(numeric)

        # then all single word answers
        single = []
        for a in answers:
            token_a = normal_tokenizer.tokenize(a)
            if len(token_a) == 1:
                single.append(a)
        single = set(single)

        for each in self.db:
            pairs = self.db[each]['QApairs']
            for pair in pairs:
                q = pair['question']
                a = pair['answer']
                t = pair['type']
                alts = []
                a = re.sub(r'-', ' - ', a)

                # if answer is yes/no
                tmp = list(single - {'yes', 'no'})
                random.shuffle(tmp)
                token_a = normal_tokenizer.tokenize(a)
                a = (' ').join([self.process(x) for x in token_a])
                pair['answer'] = a
                if token_a[0].lower() == 'yes':
                    a = 'yes'
                    alts = ['no']
                    alts += tmp[:3]
                if token_a[0].lower() == 'no':
                    a = 'no'
                    alts = ['yes']
                    alts += tmp[:3]
                if len(alts) == 4:
                    pair['alternatives'] = alts
                    continue

                if len(alts) != 0:
                    print('sanlvbi')

                # if answer is numeric
                digit_a = numeric_tokenizer.tokenize(a)
                if len(digit_a) > 0:
                    if self.types['when'] not in t and self.types['count'] in t:
                        alts = self.rand_num_in_sentence(a)
                    else:
                        tmp = list(numeric - {a})
                        random.shuffle(tmp)
                        alts = tmp[:4]
                if len(alts) == 4:
                    pair['alternatives'] = alts
                    continue

                if len(alts) != 0:
                    print('sanlvbi')

                # if answer is single word
                token_a = normal_tokenizer.tokenize(a)
                if len(token_a) == 1:
                    if token_a[0] == 'after':
                        alts = ['before']
                        tmp = list(single - {a, 'before', 'before.'})
                        random.shuffle(tmp)
                        alts += tmp[:3]
                    elif token_a[0] == 'before':
                        alts = ['after']
                        tmp = list(single - {a, 'after', 'after.'})
                        random.shuffle(tmp)
                        alts += tmp[:3]
                    else:
                        tmp = list(single - {a})
                        random.shuffle(tmp)
                        alts = tmp[:4]
                if len(alts) == 4:
                    pair['alternatives'] = alts
                    continue

                if len(alts) != 0:
                    print('sanlvbi')

                # if answer is more than single word
                # check same words, later we can test the length
                token_q = normal_tokenizer.tokenize(q)
                q = (' ').join([self.process(x) for x in token_q])
                set_q = set([self.dict_a[x] for x in token_q if x in self.dict_a])
                set_a = set([self.dict_a[x] for x in token_a if x in self.dict_a])
                tmp_alts = answers - {a}

                # same_score stores number of same words when compared with q and a
                same_score = {}
                for each in tmp_alts:
                    token = normal_tokenizer.tokenize(each)
                    set_alt = set([self.dict_a[x] for x in token if x in self.dict_a])
                    same_score[each] = len(set_q & set_alt) + len(set_a & set_alt)

                x = sorted(same_score, key=same_score.get, reverse=True)
                alts = x[:4]
                if len(alts) == 4:
                    pair['alternatives'] = alts
                    continue

                print('shabi')

        with open('qa_with_multiple_choice.json', 'w') as f:
           json.dump(self.db, f)


    def similarity_based_multiple_choice(self):
        # random pick multiple choice alternatives
        # same type, then same recipe
        # if not enough, next type and same recipe
        # still not enough, then same type different recipe
        # sort by similarity to original answer
        for each in self.db:
            pairs = self.db[each]['QApairs']
            r = self.db[each]['recipe_type']
            for pair in pairs:
                t = pair['type']
                alts = set(self.get_alternatives(t[0], r))
                i = 1
                while len(alts) < 4:
                    if len(t) == i:
                        alts2 = set(self.get_alternatives(t[0], '000'))
                    else:
                        alts2 = set(self.get_alternatives(t[-i], r))

                    i += 1
                    alts |= alts2

                alts = self.most_similar(4, alts, pair['answer'])
                assert(len(alts) == 4)
                pair['alternatives'] = alts

        with open('qa_with_multiple_choice.json', 'w') as f:
            json.dump(self.db, f)


    def visual_multiple_choice(self, type_name, num=-1):
        type_num = self.types[type_name]
        db_choice = json.load(open('cleaned_db.json', 'r'))
        all_pairs = []
        for each in db_choice:
            pairs = db_choice[each]['QApairs']
            if type_num == -1:
                all_pairs += pairs
                continue
            for pair in pairs:
                t = pair['type']
                if type_num in t:
                    all_pairs.append(pair)

        random.shuffle(all_pairs)
        for pair in all_pairs[:num]:
            alts = pair['alternatives']
            print('Q):', pair['question'])
            print('A): a.', pair['answer'])
            print('    b.', alts[0])
            print('    c.', alts[1])
            print('    d.', alts[2])
            print('    e.', alts[3])

if __name__ == '__main__':
    stats = statistics()
    # stats.similarity_based_multiple_choice()
    # stats.rule_based_multiple_choice()

    stats.qa_stats('count')
    stats.qa_stats('when')
    stats.qa_stats('order')
    stats.qa_stats('property')
    stats.qa_stats('reasoning')
    stats.qa_stats('taste')
    stats.qa_stats('total')
    stats.recipe_stats('total')
    stats.visual_multiple_choice('count', num=3)
    stats.visual_multiple_choice('when', num=3)
    stats.visual_multiple_choice('order', num=3)
    stats.visual_multiple_choice('property', num=3)
    stats.visual_multiple_choice('reasoning', num=3)
    stats.visual_multiple_choice('taste', num=3)
