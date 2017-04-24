import json
import pickle

data = pickle.load(open('project_template/qa_vec.pickle', 'rb'))
vectorizer = data['vectorizer']
matrix = data['matrix']
mapping = data['mapping'] #list of tuples (thread, answer)

threads = json.load(open('data-1000.json', 'rb'))

thread_to_index = {}
fullDocText = []
qa_idx_to_thread_idx = [] #the ith elt in this list corresponds to thread idx
#of the ith qa_pair
for idx, thread in enumerate(threads):
	thread_to_index[thread['id']] = idx
	doc_text = """"""
	doc_text += thread['text']
	doc_text += thread['title']
	for c in thread['comments']:
		doc_text += c['body']
	fullDocText += [doc_text]

for idx, qa_pair in enumerate(mapping):
	thread_id = qa_pair[0]
	qa_idx_to_thread_idx += [thread_to_index[thread_id]]


to_pickle = {'fullText': threads,
         'qa_to_thread_idx': qa_idx_to_thread_idx}

with open('fullText.pickle', 'wb') as handle:
	pickle.dump(to_pickle, handle, protocol = pickle.HIGHEST_PROTOCOL)
