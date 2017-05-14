import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
from sklearn.preprocessing import normalize as normalize
from empath import Empath
from nltk.corpus import wordnet
import numpy as np
from scipy.sparse import vstack
import os
from settings import PROJECT_ROOT
import StringIO, contextlib, sys

from project_template import UP_DATA as p
from project_template import QA_TFIDF_MAT, QA_TFIDF_VECTORIZER, QA_TFIDF_FEATURE_TO_IDX
from project_template import QA_TFIDF_IDX_TO_FEATURE, NUM_FEATURES_IN_QA
from project_template import EMPATH_MATRIX, EMP_VECTORIZER
from project_template import DOC_TFIDF_MAT, DOC_TFIDF_VECTORIZER
from project_template import LEX
from project_template import spelling

MODEL = 'reddit'
USE_WORDNET = 0
MUL = 1

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

            if synonyms == "":
                return [], None
            else:
                return [], cat

        cat_vec = normalize(DOC_TFIDF_VECTORIZER.transform([synonyms]))
        # multiply by normalized vector
        row_vec = cat_vec.dot(DOC_TFIDF_MAT.T).T.toarray().flatten()

    else:
        # spell check
        synonyms = find_syns(cat)
        if synonyms == "":
            print("no synonyms")
            cat = spelling.correction(cat)
            synonyms = find_syns(cat)

            if synonyms == "":
                return [], None, None
            return [], cat, None

        # Expand category with create_category
        with stdoutIO() as s:
            LEX.create_category(cat, [cat], model = MODEL)
        expanded_cat = s.getvalue()
        print("Non expanded cat:" + expanded_cat)
        expanded_cat = expanded_cat.replace("_", " ").replace("\"", "").replace("\\", "").replace("[", "").replace("]", "")
        print("Expanded cat: " + expanded_cat)

        emp_dict = LEX.analyze(expanded_cat)
        emp_vec = EMP_VECTORIZER.transform(emp_dict)

        row_vec = np.dot(emp_vec, EMPATH_MATRIX.T).T

    if np.sum(row_vec) == 0:
        print("Category has 0 count.")


    expanded_row_vec = np.zeros(mat.shape[0])
    # expanded_row_vec[qa_idx] = row_vec[thread_idx that qa_idx belongs to]
    for qa_idx in range(mat.shape[0]):
        expanded_row_vec[qa_idx] = row_vec[qa2thread[qa_idx]]

    q_vec = vectorizer.transform([query])
    results = cos_sim(mat, q_vec)

    if MUL:
        weighted_results = np.multiply(results, expanded_row_vec[:, np.newaxis]) #Scores
    else:
        weighted_results = results + expanded_row_vec[:, np.newaxis] #Scores

    if np.amax(weighted_results) <= 0.0:
        print("no result damnit")
        return [], None, None

    rank = np.argsort(weighted_results, axis=0)[::-1][:lim] #Indices

    mini_tfidf_mat = vstack([QA_TFIDF_MAT[idx] for idx in rank]).toarray()
    mini_tfidf_mat = np.multiply(mini_tfidf_mat, QA_TFIDF_VECTORIZER.idf_)
    #.multiply(QA_TFIDF_VECTORIZER.idf_[0])
    tfidf_sums_per_word = np.sum(mini_tfidf_mat, axis = 0)
    rank_rel_word = np.argsort(tfidf_sums_per_word, axis = 0)[::-1][:5]

    # topics = [query]
    # topic_feature_idx = [QA_TFIDF_FEATURE_TO_IDX[t] for t in topics if t in QA_TFIDF_FEATURE_TO_IDX]
    # topic_row_vec = vstack([mini_tfidf_mat[:,feature_idx] for feature_idx in topic_feature_idx])
    # cooccur_mat = topic_row_vec.T.dot(mini_tfidf_mat)
    # rank_rel_word = np.argsort(cooccur_mat)[:5]
    #
    print("=====================================")
    print(QA_TFIDF_VECTORIZER.idf_[:10])
    print(tfidf_sums_per_word[rank_rel_word])
    print([QA_TFIDF_IDX_TO_FEATURE[i] for i in rank_rel_word])
    print("=====================================")
    
    return [mapping[int(i)] for i in rank], None, [QA_TFIDF_IDX_TO_FEATURE[i] for i in rank_rel_word]

    def contains(qa_idx, words):
        for word in words:
            if QA_TFIDF_FEATURE_TO_IDX[qa_idx][word] > 0:
                return true
        return false

    def filter(words, original_results):
        to_return = []
        for idx in original_results:
            if(contains(idx, words)):
                to_return += [idx]
        return to_return
