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

vectorizer = TfidfVectorizer(min_df = 10, max_df = 0.9)
tfidf_mat = vectorizer.fit_transform(qa_list)

to_pickle = {'vectorizer': vectorizer,
             'matrix': tfidf_mat,
             'mapping': mapping}

with open("qa_vec.pickle", "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)
