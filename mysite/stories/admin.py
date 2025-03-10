from django.contrib import admin
from .models import *

admin.site.register(Stories)
admin.site.register(StoriesText)
admin.site.register(StoriesLike)
admin.site.register(CommentStories)