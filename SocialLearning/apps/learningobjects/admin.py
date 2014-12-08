from django.contrib import admin

# Register your models here.

from learningobjects.models import *

class ResourceInline(admin.TabularInline):
    model = Collection.resources.through

class CollectionAdmin(admin.ModelAdmin):
    filter_horizontal = ("resources",)
    #inlines = [ ResourceInline, ]

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Resource)
admin.site.register(ResourceContainer)
admin.site.register(SocialNetwork)
admin.site.register(Mention)
admin.site.register(Topic)
admin.site.register(Relevance)
admin.site.register(SocialProfile)



