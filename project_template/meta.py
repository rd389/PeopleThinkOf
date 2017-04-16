from project_template import DB as db

qa = db.qa
threads = db.threads

SAMPLE = [
  {'thread_id': '32qrh5', 'answer_id': 'cqe351s'},
  {'thread_id': '4fnlqd', 'answer_id': 'd2agami'},
  {'thread_id': '4fnlqd', 'answer_id': 'd2aiydl'},
  {'thread_id': '2fmrrx', 'answer_id': 'ckavtjm'},
  {'thread_id': '2rg8q3', 'answer_id': 'cnfkdrf'}
]

def get_qa_info(id_pairs=SAMPLE):
  """
  Return the QA pair docs from mongo.

  id_pairs - a list of dictionaries in the form { thread_id, answer_id }
  """
  # does this preserve order? (index scanning)
  result = list(qa.find({'$or': id_pairs}))
  titles = get_thread_title(id_pairs)

  for doc in result:
    doc['title'] = titles[doc['thread_id']]
    doc['url'] = 'https://www.reddit.com/r/IAmA/comments/' + doc['thread_id'] + '/' + doc['question_id']

  return result

def get_thread_title(id_pairs=SAMPLE):
  # TODO
  thread_ids = [{'thread_id': pair['thread_id']} for pair in id_pairs]
  # does this preserve order? (index scanning)
  thread_docs = threads.find({'$or': thread_ids}, {'thread_id': 1, 'title': 1})
  return { doc['thread_id']: doc['title'] for doc in thread_docs }
