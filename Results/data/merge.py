'''
Merge train/val/test sequentially into one matrix.
'''

import pickle
import os
import numpy as np

# files = os.listdir('training')
files = ['mat_ans_type.pkl', 'mat_type.pkl']
merged = {x: [] for x in files}
for f in files:
    for split in ['training/', 'validation/', 'testing/']:
        merged[f].append(pickle.load(open(split + f, 'rb')))

# train: (10179) val: (3481) test: (1611)
# print(merged[f][0].shape, merged[f][1].shape, merged[f][2].shape)

for f in files:
    pickle.dump(np.concatenate(merged[f]), open('all/' + f, 'wb'), protocol=2)

