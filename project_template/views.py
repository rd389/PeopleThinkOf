from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .meta import get_qa_info
# from .ir import myfunction

# Create your views here.
def index(request):
  output_list = ''
  output=''
  sample = get_qa_info()

  if request.GET.get('search'):
    query = request.GET.get('search')
    # results = myfunction(query)
    # output = get_qa_info(results)
    output = sample


    print search
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
                         'sample': sample
                         })
