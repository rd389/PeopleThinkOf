from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .meta import get_qa_info
from .ir import search, categorized_search

# Create your views here.
def index(request):
  output=''
  results_label = ""

  if request.GET.get('topic'):
    topic = request.GET.get('topic')
    desc = request.GET.get('desc')

    if desc.strip() == '':
      desc_str = 'all'
      raw_results = search(topic, lim = 20)
      
    else:
      desc_str = desc
      raw_results = categorized_search(topic, desc, lim = 20) #Current lim = 20
    
    results = [{"thread_id": res[0], "answer_id": res[1]} for res in raw_results]
    output = get_qa_info(results)
    results_label = 'Showing results for "What do {} people think about {}?" '.format(desc_str, topic)

    # print search

    # output_list = find_similar(search)
    # paginator = Paginator(output_list, 10)
    # page = request.GET.get('page')
    # try:
    #     output = paginator.page(page)
    # except PageNotAnInteger:
    #     output = paginator.page(1)
    # except EmptyPage:
    #     output = paginator.page(paginator.num_pages)
  return render_to_response('project_template/index.html', 
                        {'output': output,
                         'magic_url': request.get_full_path(),
                         'result_label': results_label,
                         })
