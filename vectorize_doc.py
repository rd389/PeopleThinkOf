import json
import sys, time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
import pickle, json
from empath import Empath
import numpy as np


"""
    Returns
     - list of docs(concat'd) and list of thread_id
"""

input_file = "./DocPickleTexts/fullText.pickle"
meta_file = "thread_meta.json"
optext_file = "./DocPickleTexts/allOPDocText.pickle"
output_file = "./project_template/thread_vec.pickle"
with open(input_file, "rb") as handle:
    data = pickle.load(handle)

with open(meta_file, "rb") as handle:
    meta = json.load(handle)

with open(optext_file, "rb") as handle:
    optext = pickle.load(handle)

N = len(data['fullText'])
assert len(optext['text']) == N

mapping = [None] * N
inv_idx = {}
emp_dicts = [None] * N

t0 = time.time()
for idx, thread in enumerate(meta):
    mapping[idx] = thread['thread_id']
    inv_idx[thread['thread_id']] = idx

vectorizer = TfidfVectorizer(min_df = 10, max_df = 0.9)
tfidf_mat = vectorizer.fit_transform(optext['text'])

t1 = time.time()
print("Index mapping time: " + str(t1-t0))
lex = Empath()
for i in range(N):
    emp_dicts[i] = lex.analyze(data['fullText'][i])

dvec = DictVectorizer(sparse = False)
emp_mat = dvec.fit_transform(emp_dicts)
t2 = time.time()

print("Empath comp time: " + str(t2-t1))

to_pickle = {'idx_map': mapping,
             'inv_idx': inv_idx,
             'emp_mat': emp_mat,
             'dict_vect': dvec,
             'tfidf_mat': tfidf_mat,
             'tfidf_vectorizer': vectorizer}


with open(output_file, "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)

t3 = time.time()
print("Pickling time: " + str(t3-t2))
