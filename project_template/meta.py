from project_template import DB as db

qa = db.qa
threads = db.threads

SAMPLE = [
  {'thread_id': '32qrh5', 'answer_id': 'cqe351s'},
  {'thread_id': '4fnlqd', 'answer_id': 'd2agami'},
  {'thread_id': '4fnlqd', 'answer_id': 'd2aiydl'},
  {'thread_id': '2fmrrx', 'answer_id': 'ckavtjm'},
  {'thread_id': '3zxrf3', 'answer_id': 'cypwepq'}
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

    # FIXME: need to handle deleted posts, which still have permalinks...
    if doc['question_id'] == None:
      comment_id = doc['answer_id']
    else:
      comment_id = doc['question_id']
      if len(doc['question_text']) == 0:
        print comment_id

    doc['url'] = 'https://www.reddit.com/r/IAmA/comments/' + doc['thread_id'] + '/_/' + comment_id
    doc['sent_score'] = round(doc['sentiment']['compound'], 2)

    # TODO: need to add a tooltip or something to explain these scores
    if doc['sent_score'] > 0:
      doc['sent_score'] = '+' + str(doc['sent_score'])

    if doc['sentiment']['compound'] < -0.5:
      doc['sent_label'] = 'negative'

    elif doc['sentiment']['compound'] > 0.5:
      doc['sent_label'] = 'positive'

    else:
      doc['sent_label'] = 'neutral'


  return result

def get_thread_title(id_pairs=SAMPLE):
  # TODO
  thread_ids = [{'thread_id': pair['thread_id']} for pair in id_pairs]
  # does this preserve order? (index scanning)
  thread_docs = threads.find({'$or': thread_ids}, {'thread_id': 1, 'title': 1})
  return { doc['thread_id']: doc['title'] for doc in thread_docs }
