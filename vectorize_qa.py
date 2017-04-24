<<<<<<< HEAD
import json, pickle
import sys, time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from empath import Empath


with open("qa.json", "rb") as handle:
    j = json.load(handle)

with open("./project_template/thread_vec.pickle", "rb") as handle:
    thread_meta = pickle.load(handle)

qa_list = [None] * len(j)
mapping = [None] * len(j)
qa_idx_2_thread = [0] * len(j) # inv_map[] = qa's idx

# Concat QnA texts and get index to (thread_id, answer_id) map (in array form)
#   and gather empath analysis
lex = Empath()
t1 = time.time()
for idx, qa in enumerate(j):
    qa_list[idx] = qa["question_text"] + " " + qa["answer_text"]
    mapping[idx] = (qa["thread_id"], qa["answer_id"])
    qa_idx_2_thread[idx] = thread_meta["inv_idx"][qa["thread_id"]]

t2 = time.time()

print("Compilation time: " + str(t2-t1))
=======
import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

handle = open("qa.json")
j = json.load(handle)

qa_list = [None] * len(j)
mapping = [None] * len(j)
for idx, qa in enumerate(j):
    qa_list[idx] = qa["question_text"] + " " + qa["answer_text"]
    mapping[idx] = (qa["thread_id"], qa["answer_id"])
>>>>>>> 51aa5eb43beb3ad994ff22e6206f6078cfb5ad65

vectorizer = TfidfVectorizer(min_df = 10, max_df = 0.9)
tfidf_mat = vectorizer.fit_transform(qa_list)

to_pickle = {'vectorizer': vectorizer,
             'matrix': tfidf_mat,
<<<<<<< HEAD
             'mapping': mapping,
             'qa2thread': qa_idx_2_thread}

with open("./project_template/qa_vec.pickle", "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)

t3 = time.time()
print("Pickle time: " + str(t3 - t1))
=======
             'mapping': mapping}

with open("qa_vec.pickle", "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)
>>>>>>> 51aa5eb43beb3ad994ff22e6206f6078cfb5ad65
