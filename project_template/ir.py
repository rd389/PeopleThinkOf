import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
import numpy as np
import os
from settings import PROJECT_ROOT
from project_template import UP_DATA as p
from project_template import MATRIX, CAT_LOOKUP

def search(query, lim=20):
    vectorizer = p['vectorizer']
    mat = p['matrix']
    mapping = p['mapping']
    q_vec = vectorizer.transform([query])
    results = cos_sim(mat, q_vec)
    rank = np.argsort(results, axis=0)
    rank = rank[::-1][:lim]
    results = [mapping[int(i)] for i in rank]
    return results


def categorized_search(query, cat, lim=20):
    vectorizer = p['vectorizer']
    mat = p['matrix']
    mapping = p['mapping']
    q_vec = vectorizer.transform([query])
    results = cos_sim(mat, q_vec)
    #NEED TO IMPORT MATRIX & category lookup
    cat_vec = MATRIX[CAT_LOOKUP[cat]].T
    print(CAT_LOOKUP[cat])
    results = np.multiply(results, cat_vec)
    #may want to define the weighting we will use
    rank = np.argsort(results, axis=0)
    rank = rank[::-1][:lim]
    results = [mapping[int(i)] for i in rank]

    return results
