from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .meta import get_qa_info
from .ir import search

# Create your views here.
def index(request):
  output=''
  sample = get_qa_info()
  results_label = ""

  if request.GET.get('search'):
    query = request.GET.get('search')
    raw_results = search(query, lim = 20) #Current lim = 20
    results = [{"thread_id": res[0], "answer_id": res[1]} for res in raw_results]
    output = get_qa_info(results)

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
                         'sample': sample,
                         'result_label': results_label,
                         'query': query
                         })
