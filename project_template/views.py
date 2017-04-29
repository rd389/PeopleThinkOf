from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .meta import get_qa_info
from .ir import search, categorized_search, search_emp

# Create your views here.
def index(request):
  output=''
  results_label = ""
  output_header_class = 'hide'
  showing_or_no = 'hide'

  if request.GET.get('topic'):
    topic = request.GET.get('topic')
    desc = request.GET.get('desc')

    if desc.strip() == '':
      desc_str = 'all'
      raw_results = search(topic, lim = 20)

    else:
      desc_str = desc
      # raw_results = categorized_search(topic, desc, lim = 20) #Current lim = 20
      raw_results = search_emp(topic, desc, lim=20)

    results_label = 'What do {} people think about {}?'.format(desc_str, topic)
    output_header_class = 'show'

    if len(raw_results) == 0:
      showing_or_no = 'No'

    else:
      results = [{"thread_id": res[0], "answer_id": res[1]} for res in raw_results]
      output = get_qa_info(results)
      # TEMPORARY FIX: Ignore ones that don't have question_text
      # (should be fixed in data fetching part)
      output = [item for item in output if len(item['question_text']) > 0]
      
      showing_or_no = 'Showing'

  return render_to_response('project_template/index.html', 
                        {'output': output,
                         'magic_url': request.get_full_path(),
                         'result_label': results_label,
                         'output_header_class': output_header_class,
                         'showing_or_no': showing_or_no
                         })
