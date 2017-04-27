import json
import sys, time
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle, json
from empath import Empath
import numpy as np


"""
    Returns
     - list of docs(concat'd) and list of thread_id
"""
EMP_LEN = 194

def emp2vec(d):
    assert len(d) == EMP_LEN
    return [score for score in d.values()]

input_file = "fullText.pickle"
meta_file = "thread_meta.json"
output_file = "./project_template/thread_vec.pickle"
with open(input_file, "rb") as handle:
    data = pickle.load(handle)

with open(meta_file, "rb") as handle:
    meta = json.load(handle)

# corpus = [None] * len(data)
N = len(data['fullText'])
mapping = [None] * N
inv_idx = {}

emp_mat = np.zeros((N, EMP_LEN))

t0 = time.time()
for idx, thread in enumerate(meta):
    mapping[idx] = thread['thread_id']
    inv_idx[thread['thread_id']] = idx

# vectorizer = TfidfVectorizer(min_df = 10, max_df = 0.9)
# tfidf_mat = vectorizer.fit_transform(corpus)

t1 = time.time()
print("Index mapping time: " + str(t1-t0))
lex = Empath()
for i in range(N):
    emp_mat[i] = emp2vec(lex.analyze(data['fullText'][i]))
# emp_map = [{k: v for k, v in lex.analyze(d).items() if v > 0} for d in data['fullText']]
t2 = time.time()

print("Empath comp time: " + str(t2-t1))

to_pickle = {'idx_map': mapping,
             'inv_idx': inv_idx,
             'emp_mat': emp_mat}


with open(output_file, "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)

t3 = time.time()
print("Pickling time: " + str(t3-t2))
