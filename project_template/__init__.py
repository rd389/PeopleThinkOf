import pymongo, os, pickle
import numpy as np
from empath import Empath
from settings import PROJECT_ROOT

MONGO_CLIENT = pymongo.MongoClient(os.environ['MONGODB_URI'])
DB = MONGO_CLIENT[os.environ['MONGODB_DB_NAME']]

with open(os.path.join(PROJECT_ROOT,"qa_vec.pickle"), "rb") as handle:
    UP_DATA = pickle.load(handle)

with open(os.path.join(PROJECT_ROOT,"thread_vec.pickle"), "rb") as handle:
    EMPATH_MATRIX = np.array(pickle.load(handle)['emp_mat'])

#LOAD MATRIX DATA HERE
with open(os.path.join(PROJECT_ROOT,"default_cats_matrix.pickle"), "rb") as handle:
    matrix_data= pickle.load(handle)
    MATRIX = matrix_data["matrix"]
    CAT_LOOKUP = matrix_data["lookup"]

LEX = Empath()
IDX_TO_CAT = LEX.analyze("")
CAT_TO_IDX = {cat: idx for idx, cat in enumerate(IDX_TO_CAT)}
EMP_LEN = len(IDX_TO_CAT)

print(EMP_LEN)
