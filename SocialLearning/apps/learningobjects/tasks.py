from __future__ import absolute_import

from celery import shared_task
from learningobjects.models import Resource

@shared_task
def test(param):
    return 'social learning is working "%s" ' % param

@shared_task
def describe(id):
    try:

        res = Resource.objects.get(pk=id)
        res.describe()
        res.save()

        msg = 'social learning processed resource "%s" ' % res.title
    except:
        msg = 'social learning failed processing resource "%s" ' % res.title

    return msg