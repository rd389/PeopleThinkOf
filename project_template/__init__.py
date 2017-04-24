import pymongo, os, pickle
from empath import Empath
from settings import PROJECT_ROOT

MONGO_CLIENT = pymongo.MongoClient(os.environ['MONGODB_URI'])
DB = MONGO_CLIENT[os.environ['MONGODB_DB_NAME']]
with open(os.path.join(PROJECT_ROOT,"qa_vec.pickle"), "rb") as handle:
    UP_DATA = pickle.load(handle)

with open(os.path.join(PROJECT_ROOT,"thread_vec.pickle"), "rb") as handle:
    EMPATH_MATRIX = pickle.load(handle)['emp_mat']
LEX = Empath()

#LOAD MATRIX DATA HERE
with open(os.path.join(PROJECT_ROOT,"default_cats_matrix.pickle"), "rb") as handle:
    matrix_data= pickle.load(handle)
    MATRIX = matrix_data["matrix"]
    CAT_LOOKUP = matrix_data["lookup"]
