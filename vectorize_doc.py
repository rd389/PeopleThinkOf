import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

"""
    Returns
     - list of docs(concat'd) and list of thread_id
"""
def json_to_docs(data):
    corpus = [None] * len(data)
    mapping = [None] * len(data)

    for idx, thread in enumerate(data):
        corpus[idx] = thread['text'] + " "
        mapping[idx] = thread['thread_id']

        for c in thread['comments']:
            corpus[idx] += c['body'] + " "

    return corpus, mapping

input_file = "threads.json"
output_file = "vec_threads.pickle"
with open(input_file, "rb") as handle:
    data = json.load(handle)

corpus, mapping = json_to_docs(data)

vectorizer = TfidfVectorizer(min_df = 10, max_df = 0.9)
tfidf_mat = vectorizer.fit_transform(corpus)

to_pickle = {'vectorizer': vectorizer,
             'matrix': tfidf_mat,
             'idx_map': mapping}

with open(output_file, "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)
