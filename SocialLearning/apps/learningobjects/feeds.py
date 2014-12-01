from django.core.exceptions import ObjectDoesNotExist
from learningobjects.models import Collection, Resources
from django.contrib.syndication.feeds import Feed

class CollectionFeed(Feed):
    def get_object(self, bits):
        # In case of "/feeds/tags/cats/dogs/mice/", or other such
        # clutter, check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Collection.objects.get(tag=bits[0])

    def title(self, obj):
        return "My Blog: Entries tagged with %s" % obj.tag

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Entries tagged with %s" % obj.tag

    def items(self, obj):
        entries = Resource.objects.filter(collection__id__exact=obj.id)
        return entries.order_by('-pub_date')[:30]