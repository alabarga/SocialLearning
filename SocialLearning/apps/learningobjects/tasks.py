from __future__ import absolute_import

from celery import shared_task
from learningobjects.models import Resource
from learningobjects.social import *

@shared_task
def test(param):
    return 'social learning is working "%s" ' % param

@shared_task
def describe(id):
    try:

        res = Resource.objects.get(pk=id)
        res.describe()
        res.save()

        find_mentions.delay(id)

        msg = 'social learning processed resource "%s" ' % res.title
    except:
        msg = 'social learning failed processing resource "%s" ' % res.title

    return msg

@shared_task
def find_mentions(id):

    res = Resource.objects.get(pk=id)

    t = Twitter()
    d = Delicious()

    ss = [t, d]

    for s in ss:
        try:        

            mentions = s.find_mentions(res.url)

            sn=SocialNetwork.objects.get_or_create(name=s.name,url=s.url)[0]
            for m in mentions:        
                author = m['username']
                sp=SocialProfile.objects.get_or_create(username=author, social_network=sn, url=s.profile_url(author))
                mt=Mention.objects.get_or_create(profile=sp[0],resource=res)[0]
                for tag in m['tags']:
                    mt.tags.add(tag)

            msg = 'social learning processed resource "%s" for mentions' % res.title
        except:
            continue
            msg = 'social learning failed processing resource "%s" for mentions' % res.title

    res.status = Resource.DISCOVERED
    res.save()
    return msg   
