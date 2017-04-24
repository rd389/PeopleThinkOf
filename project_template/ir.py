import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
import numpy as np
import os
from settings import PROJECT_ROOT
from project_template import UP_DATA as p
<<<<<<< HEAD
from project_template import EMPATH_MATRIX as emp_mat
from empath import Empath

def emp2vec(d):
    assert len(d) == EMP_LEN
    return [score for score in d.values()]
=======
from project_template import MATRIX, CAT_LOOKUP
>>>>>>> 51aa5eb43beb3ad994ff22e6206f6078cfb5ad65

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

<<<<<<< HEAD
def search_emp(query, lim = 20):
    q = query.split(";;")
    vectorizer = p['vectorizer']
    mat = p['matrix']
    mapping = p['mapping']
    emp_dict = LEX.analyze(q[0], normalize=True)
    # list of category indices whose count is >0
    cat_list = [score for _, score in emp_dict.items() if score > 0]
    # numpy-fy
    np_emp_mat = np.array(emp_mat)

    emp_vec_list = [np_emp_mat[:, cat] for cat in cat_list]
    cats_vec = emp2vec(emp_dict)

    #weighted_results = np.multiply(results, b[])
=======

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
>>>>>>> 51aa5eb43beb3ad994ff22e6206f6078cfb5ad65
