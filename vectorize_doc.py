import codecs, json
import nltk
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

"""

"""
def json_to_docs(data):
    corpus = [None] * len(data)

    for idx, thread in enumerate(data):
        corpus[idx] = thread['text'] + " "

        for c in thread['comments']:
            corpus[idx] += c['body'] + " "

    return corpus

if not len(sys.argv) == 3:
    print sys.argv
    raise Exception("I need exactly two buddy; you gave me: " + str(len(sys.argv)))

if not sys.argv[1][-5:] == ".json":
    raise Exception("I need a .json file buddy")

if not sys.argv[2][-7:] == ".pickle":
    raise Exception("I need a .pickle file buddy")

input_file = sys.argv[1]
output_file = sys.argv[2]
f = open(input_file)
data = json.load(f)

corpus = json_to_docs(data)

vectorizer = TfidfVectorizer(min_df = 10, max_df = 0.9)
tfidf_mat = vectorizer.fit_transform(corpus)

to_pickle = {'vectorizer': vectorizer, 'matrix': tfidf_mat}

with open(output_file, "wb") as handle:
    pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)
