from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from utils.search import *
from random import shuffle

def search_form(request):
  return render(request, 'learningobjects/search.html')

def search(request):
  if 'q' in request.GET:
    if request.GET['q'] == '':
      message = 'No searching keyword entered'
    else:
      results=[]
      message = 'You searched for: %s' % request.GET['q']
      #no funciong=Google()
      d=DuckDuckGoIO()
      s=Slideshare()
      engines=[d,s]
      for engine in engines:
        links=engine.search(request.GET['q'])
        #for index in range(len(links)):
        #  links[index]=engine.clean(links[index]) el unfurl aveces no funciona
        results+=links
      shuffle(results)

  else:
      message = 'Form is not submitted properly.'
  return render(request, "learningobjects/results.html",
                {
                    'results':results[:10],
                    'message':message,
                }) 