import pymongo, os, pickle
import numpy as np
from empath import Empath
from settings import PROJECT_ROOT
import spelling

MONGO_CLIENT = pymongo.MongoClient(os.environ['MONGODB_URI'])
DB = MONGO_CLIENT[os.environ['MONGODB_DB_NAME']]

with open(os.path.join(PROJECT_ROOT,"qa_vec.pickle"), "rb") as handle:
    UP_DATA = pickle.load(handle)

with open(os.path.join(PROJECT_ROOT,"thread_vec.pickle"), "rb") as handle:
    THREAD_VEC = pickle.load(handle)
    EMPATH_MATRIX = np.array(THREAD_VEC['emp_mat'])
    EMP_VECTORIZER = THREAD_VEC['dict_vect']
    DOC_TFIDF_MAT = THREAD_VEC['tfidf_mat']
    DOC_TFIDF_VECTORIZER = THREAD_VEC['tfidf_vectorizer']

LEX = Empath()
