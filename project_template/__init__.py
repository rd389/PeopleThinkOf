import pymongo, os, pickle

MONGO_CLIENT = pymongo.MongoClient(os.environ['MONGODB_URI'])
DB = MONGO_CLIENT[os.environ['MONGODB_DB_NAME']]
with open("qa_vec.pickle", "rb") as handle:
    UP_DATA = pickle.load(handle)
