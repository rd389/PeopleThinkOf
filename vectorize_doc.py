import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

"""
    Returns
     - list of docs(concat'd) and list of thread_id
"""

def compress_emp_list(d):
    return {k: v for k, v in d.items() if v > 0}

input_file = "threads.json"
output_file = "vec_threads.pickle"
with open(input_file, "rb") as handle:
    data = json.load(handle)

corpus = [None] * len(data)
mapping = [None] * len(data)
inv_idx = {}
emp_map = [None] * len(data)

for idx, thread in enumerate(data):
    corpus[idx] = thread['text'] + " "
    mapping[idx] = thread['thread_id']
    inv_idx[thread['thread_id']] = idx

    for c in thread['comments']:
        corpus[idx] += c['body'] + " "

vectorizer = TfidfVectorizer(min_df = 10, max_df = 0.9)
tfidf_mat = vectorizer.fit_transform(corpus)

t1 = time.time()
emp_map = [{k: v for k, v in lex.analyze(d).items() if v > 0} for d in corpus]
t2 = time.time()

print("Empath comp time: " + str(t2-t1))

to_pickle = {'vectorizer': vectorizer,
             'matrix': tfidf_mat,
             'idx_map': mapping,
             'inv_idx': inv_idx,
             'emp_map': emp_map}

with open(output_file, "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)

t3 = time.time()
pritn("Pickling time: " + str(t3-t2))
