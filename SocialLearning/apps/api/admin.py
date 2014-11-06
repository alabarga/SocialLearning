from django.contrib import admin

# Register your models here.

from learningobjects.models import *

admin.site.register(Resource)
admin.site.register(Collection)
admin.site.register(SocialNetwork)
admin.site.register(Mention)
admin.site.register(SocialProfile)



