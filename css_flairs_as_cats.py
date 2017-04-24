import pickle
import numpy as np
import json

data = pickle.load(open('project_template/qa_vec.pickle', 'rb'))
vectorizer = data['vectorizer']
matrix = data['matrix']
mapping = data['mapping']

threads = json.load(open('data-1000.json', 'rb'))
categories = {}

for idx, thread in enumerate(threads):
	categories[thread["id"]] = thread["category"]

unique_cats = set(categories.values())
category_to_index = {cat: index for index, cat in enumerate(unique_cats)}
matrix = np.zeros((len(unique_cats), len(mapping)))

for idx, qa_pair in enumerate(mapping):
	thread_id = qa_pair[0]
	cat = categories[thread_id]
	matrix[category_to_index[cat]][idx] = 1

with open('default_cats_matrix.pickle', 'wb') as handle:
	pickle.dump(matrix, handle, protocol = pickle.HIGHEST_PROTOCOL)

with open('default_cats_autocomplete.json', 'wb') as autocompleteObj:
	to_pickle = {key: "null" for key in unique_cats}
	autocompleteObj.write(json.dumps(to_pickle))




