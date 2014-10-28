from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

def search_form(request):
  return render(request, 'learningobjects/search.html')

def search(request):
  if 'q' in request.GET:
    if request.GET['q'] == '':
      message = 'No searching keyword entered'
    else:
      message = 'You searched for: %s' % request.GET['q']
  else:
      message = 'Form is not submitted properly.'
  return render(request, "learningobjects/results.html",
                {
                    'message':message,
                }) 