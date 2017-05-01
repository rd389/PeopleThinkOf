import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
from sklearn.preprocessing import normalize as normalize
from empath import Empath
from nltk.corpus import wordnet
import numpy as np
import os
from settings import PROJECT_ROOT
import StringIO, contextlib, sys

from project_template import UP_DATA as p
from project_template import EMPATH_MATRIX, EMP_VECTORIZER
from project_template import DOC_TFIDF_MAT, DOC_TFIDF_VECTORIZER
from project_template import MATRIX, CAT_LOOKUP, CAT_TO_IDX, IDX_TO_CAT, LEX
from project_template import spelling

MODEL = 'reddit'
USE_WORDNET = 1
MUL = 0

"""
    Taken from stackoverflow to catch the output to stdio to my own var
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
    if np.amax(results) <= 0.0:
        return []
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
    cat_vec = MATRIX[CAT_LOOKUP[cat]]

    results = results[:, 0] * cat_vec

    #may want to define the weighting we will use
    rank = np.argsort(results, axis=0)
    rank = rank[::-1][:lim]
    results = [mapping[int(i)] for i in rank]

    return results

def find_syns(word):
    synonyms = ""
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms += l.name() + ", "
    print(synonyms)
    return synonyms

def search_emp(query, cat, lim = 20):

    vectorizer = p['vectorizer']
    mat = p['matrix']
    mapping = p['mapping']
    qa2thread = p['qa2thread']

    ## Use empath analyze to get category analysis on expanded category
    if USE_WORDNET:
        # Gather synonyms
        synonyms = find_syns(cat)
        if synonyms == "":
            print("no synonyms")
            cat = spelling.correction(cat)
            synonyms = find_syns(cat)

        cat_vec = normalize(DOC_TFIDF_VECTORIZER.transform([synonyms]))
        # multiply by normalized vector
        row_vec = cat_vec.dot(DOC_TFIDF_MAT.T).T.toarray().flatten()

    else:
        # Expand category with create_category
        with stdoutIO() as s:
            LEX.create_category(cat, [cat], model = MODEL)
        expanded_cat = s.getvalue()
        print("Non expanded cat:" + expanded_cat)
        expanded_cat = expanded_cat.replace("_", " ").replace("\"", "").replace("\\", "").replace("[", "").replace("]", "")
        print("Expanded cat: " + expanded_cat)

        emp_dict = LEX.analyze(expanded_cat)
        emp_vec = EMP_VECTORIZER.transform(emp_dict)

        row_vec = np.dot(emp_vec/np.sqrt(emp_vec.dot(emp_vec.T)), EMPATH_MATRIX.T).T

    if np.sum(row_vec) == 0:
        print("Category has 0 count.")


    expanded_row_vec = np.zeros(mat.shape[0])
    # expanded_row_vec[qa_idx] = row_vec[thread_idx that qa_idx belongs to]
    for qa_idx in range(mat.shape[0]):
        expanded_row_vec[qa_idx] = row_vec[qa2thread[qa_idx]]

    q_vec = vectorizer.transform([query])
    results = normalize(cos_sim(mat, q_vec))

    if MUL:
        weighted_results = np.multiply(results, expanded_row_vec[:, np.newaxis]) #Scores
    else:
        weighted_results = results + expanded_row_vec[:, np.newaxis] #Scores

    # if np.amax(weighted_results) <= 0.0:
    #     print("no result damnit")
    #     return []

    rank = np.argsort(weighted_results, axis=0)[::-1][:lim] #Indices

    return [mapping[int(i)] for i in rank]
