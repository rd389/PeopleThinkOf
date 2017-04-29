import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
from empath import Empath
import numpy as np
import os
from settings import PROJECT_ROOT
import StringIO, contextlib, sys

from project_template import UP_DATA as p
from project_template import EMPATH_MATRIX as emp_mat
from project_template import MATRIX, CAT_LOOKUP, CAT_TO_IDX, IDX_TO_CAT, LEX, EMP_LEN

MODEL = 'reddit'

def emp2vec(d):
    assert len(d) == EMP_LEN
    emp_vec = [score for score in d.values()]
    print("================================")   
    print(len(emp_vec))
    print("================================")
    return np.array(emp_vec)/sum(emp_vec)

"""
    Taken from
"""
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


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

    with stdoutIO() as s:
        LEX.create_category(cat, [cat], model = MODEL)
    expanded_cat = s.getvalue()

    concat_exp_cat = ""
    for entry in expanded_cat:
        concat_exp_cat += entry + ", "

    emp_dict = LEX.analyze(concat_exp_cat, normalize=True)
    emp_vec = emp2vec(emp_dict)
    if sum(emp_vec) == 0:
        print("Category has 0 count.")

    row_vec = np.zeros(emp_mat.shape[0])
    for cat_idx, w in enumerate(emp_vec):
        row_vec += emp_mat[:, cat_idx] * w

    expanded_row_vec = np.zeros(mat.shape[0])
    # expanded_row_vec[qa_idx] = row_vec[thread_idx that qa_idx belongs to]
    for qa_idx in range(mat.shape[0]):
        expanded_row_vec[qa_idx] = row_vec[qa2thread[qa_idx]]

    q_vec = vectorizer.transform([query])
    results = cos_sim(mat, q_vec)
    weighted_results = np.multiply(results, expanded_row_vec[:, np.newaxis])
    rank = np.argsort(weighted_results, axis=0)[::-1][:lim]

    return [mapping[int(i)] for i in rank]
