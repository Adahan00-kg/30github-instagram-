from django.contrib import admin
from .models import PostTitle,PostImg,Comment,LikeComment,LikePost

admin.site.register(PostTitle)
admin.site.register(PostImg)
admin.site.register(Comment)
admin.site.register(LikeComment)
admin.site.register(LikePost)


