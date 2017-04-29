
def cat_sents(output):
  """
  Return a list of dictionaries {'reddit_category', 'sent_score'},
  ranked by the frequency of reddit_category in the original output

  output: original output from meta.get_qa_info()
  """

  top_cats = sorted(output, key=lambda k: k['category'])


  cats_to_sents = {}

  for item in output:
    if item['category'] not in cats_to_sents:
      cats_to_sents[item['category']] = [float(item['sent_score'])]
    else:
      cats_to_sents[item['category']].append(float(item['sent_score']))

  top_cats = sorted(cats_to_sents, key=lambda k: len(cats_to_sents[k]), reverse=True)
  print top_cats

  result = []

  for cat in top_cats:
    sent_scores = cats_to_sents[cat]
    avg_sent_score = round(1.0 * sum(sent_scores) / len(sent_scores), 2)

    if avg_sent_score > 0:
      avg_sent_score = '+' + str(avg_sent_score)
      color = 'positive'
    elif avg_sent_score < 0:
      color = 'negative'
    else:
      color = 'neutral'

    result.append({'category': cat, 'sent_score': avg_sent_score, 'color': color})

  return result
