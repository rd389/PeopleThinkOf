from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .meta import get_qa_info
from .ir import search, search_emp
from .sent import cat_sents


# Create your views here.
def index(request):
  output=''
  no_results_class = 'hide'
  subheader_class = 'hide'
  desc_str = ''
  topic = ''
  result_label = ''
  top_cats_sents = []
  corr_desc = None
  corr_query = ''

  if request.GET.get('topic'):
    topic = request.GET.get('topic')
    desc = request.GET.get('desc')

    if desc.strip() == '' or desc.strip().lower() == 'all':
      desc_str = 'all'
      raw_results = search(topic, lim = 20)

    else:
      desc_str = desc
      # raw_results = categorized_search(topic, desc, lim = 20) #Current lim = 20
      raw_results, corr_desc, rel_words, orig_rank = search_emp(topic, desc, lim=20)
      ###################################^^^^^^^^^##################################
      ################################YOU FEED THIS INTO FILTER()###################
      ################################LIKE THIS: ###################################
      ##################################FILTERED_RESULT = FILTER(WORDS, orig_rank)##

    if corr_desc is not None:
      corr_query = 'What do {} people think of {}?'.format(corr_desc, topic)

    result_label = 'What do {} people think of {}?'.format(desc_str, topic)

    no_results_class = 'hide'
    subheader_class = 'show'

    if len(raw_results) == 0:
      no_results_class = 'show'
      subheader_class = 'hide'

    else:
      results = [{"thread_id": res[0], "answer_id": res[1]} for res in raw_results]

      # fetch meta data from mongo
      output = get_qa_info(results)

      # TEMPORARY FIX: Ignore ones that don't have question_text
      # (should be fixed in data fetching part)
      output = [item for item in output if len(item['question_text']) > 0]

      # "Overall" sentiment score for the top 3 reddit categories in the results
      top_cats_sents = cat_sents(output)[:3]

      no_results_class = 'hide'
      subheader_class = 'show'

    print topic

  return render_to_response('project_template/index.html',
                        {'output': output,
                         'magic_url': request.get_full_path(),
                         'no_results_class': no_results_class,
                         'subheader_class': subheader_class,
                         'top_cats_sents': top_cats_sents,
                         'desc_str': desc_str,
                         'topic': topic,
                         'result_label': result_label,
                         'corr_query': corr_query,
                         'corr_desc': corr_desc
                         })
