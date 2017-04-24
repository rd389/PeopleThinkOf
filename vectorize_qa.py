import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from empath import Empath
import time

with open("qa.json", "rb") as handle:
    j = json.load(handle)

with open("thread_vec.pickle", "rb") as handle:
    qas = pickle.load(handle)

qa_list = [None] * len(j)
mapping = [None] * len(j)
inv_map = {}

# Concat QnA texts and get index to (thread_id, answer_id) map (in array form)
#   and gather empath analysis
lex = Empath()
t1 = time.time()
for idx, qa in enumerate(j):
    qa_list[idx] = qa["question_text"] + " " + qa["answer_text"]
    mapping[idx] = (qa["thread_id"], qa["answer_id"])

t2 = time.time()

print("Compilation time: " + str(t2-t1))

vectorizer = TfidfVectorizer(min_df = 10, max_df = 0.9)
tfidf_mat = vectorizer.fit_transform(qa_list)

to_pickle = {'vectorizer': vectorizer,
             'matrix': tfidf_mat,
             'mapping': mapping}

with open("qa_vec.pickle", "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)

t3 = time.time()
print("Pickle time: " + str(t3 - t1))
