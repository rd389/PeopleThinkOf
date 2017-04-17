import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
import numpy as np
import os
from settings import PROJECT_ROOT

def search(query, lim=20):
    with open(os.path.join(PROJECT_ROOT, 'qa_vec.pickle'), 'rb') as fp:
        p = pickle.load(fp)
    vectorizer = p['vectorizer']
    mat = p['matrix']
    mapping = p['mapping']
    q_vec = vectorizer.transform([query])
    results = cos_sim(mat, q_vec)
    rank = np.argmax(results, axis=1)
    rank = rank[::-1][:lim]
    results = [mapping[i] for i in rank]
    return results
