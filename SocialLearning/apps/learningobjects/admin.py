from django.contrib import admin

# Register your models here.

from learningobjects.models import *

class ResourceInline(admin.StackedInline):
    model = Collection.resources.through

class TopicInline(admin.StackedInline):
    model = Topic
    extra = 0

class FilesInline(admin.StackedInline):
    model = File
    extra = 0

class CollectionAdmin(admin.ModelAdmin):
    filter_horizontal = ("resources",)
    inlines = [ TopicInline, FilesInline]

class ResourceAdmin(admin.ModelAdmin):
    list_display = ("identifier","title")
    list_filter = ("status",)
    search_fields = ("identifier","title","description")

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceContainer)
admin.site.register(SocialNetwork)
admin.site.register(Mention)
admin.site.register(Topic)
admin.site.register(Relevance)
admin.site.register(SocialProfile)
admin.site.register(File)



