import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
from empath import Empath
import numpy as np
import os
from settings import PROJECT_ROOT

from project_template import UP_DATA as p
from project_template import EMPATH_MATRIX as emp_mat
from project_template import MATRIX, CAT_LOOKUP, CAT_TO_IDX, IDX_TO_CAT, LEX


def emp2vec(d):
    assert len(d) == EMP_LEN
    return [score for score in d.values()]


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
    print('results.shape')
    print(results.shape)
    #NEED TO IMPORT MATRIX & category lookup
    cat_vec = MATRIX[CAT_LOOKUP[cat]]
    print('cat_vec.shape')
    print(cat_vec.shape)
    results = results[:, 0] * cat_vec
    print(results.shape)
    #may want to define the weighting we will use
    rank = np.argsort(results, axis=0)
    rank = rank[::-1][:lim]
    results = [mapping[int(i)] for i in rank]

    return results

def search_emp(query, cat, lim = 20):

    vectorizer = p['vectorizer']
    mat = p['matrix']
    mapping = p['mapping']
    qa2thread = p['qa2thread']

    emp_dict = LEX.analyze(cat, normalize=True)
    category = max(emp_dict, key=emp_dict.get)
    
    if emp_dict[category] == 0:
        print("Category has 0 count.")
    category_idx = CAT_TO_IDX[category]

    row_vec = emp_mat[:, category_idx]
    expanded_row_vec = np.zeros(mat.shape[0])
    # expanded_row_vec[qa_idx] = row_vec[thread_idx that qa_idx belongs to]
    for qa_idx in range(mat.shape[0]):
        expanded_row_vec[qa_idx] = row_vec[qa2thread[qa_idx]]

    q_vec = vectorizer.transform([query])
    results = cos_sim(mat, q_vec)
    weighted_results = np.multiply(results, expanded_row_vec[:, np.newaxis])
    rank = np.argsort(weighted_results, axis=0)[::-1][:lim]

    return [mapping[int(i)] for i in rank if weighted_results[int(i)] > 0.0]
